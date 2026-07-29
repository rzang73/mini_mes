from abc import ABC, abstractmethod
import pandas as pd
import streamlit as st

from src import queries

# DB 모듈 안전 임포트
try:
    from src.db import DB_PATH, initialize_database
except ImportError:
    try:
        from src.db import DB_PATH, init_db as initialize_database
    except ImportError:
        from src.db import DB_PATH

        def initialize_database():
            pass


# ==========================================
# 1. Strategy Interfaces & Implementations
# ==========================================

class DataFetcherStrategy(ABC):
    """데이터 조회를 위한 전략 인터페이스"""
    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass


class ProductionQueryStrategy(DataFetcherStrategy):
    """생산실적 데이터 쿼리 전략 (여러 후보 함수를 안전하게 탐색)"""
    def __init__(self, query_names: list[str]):
        self.query_names = query_names

    def fetch(self) -> pd.DataFrame:
        for name in self.query_names:
            if hasattr(queries, name):
                try:
                    res = getattr(queries, name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        return res
                except Exception:
                    continue

        return pd.DataFrame(columns=[
            "production_no", "order_no", "item_code", "item_name",
            "fg_lot_no", "good_qty", "defect_qty", "yield_rate", "production_date"
        ])


class FilterStrategy(ABC):
    """데이터 필터링 전략 인터페이스"""
    @abstractmethod
    def filter(self, df: pd.DataFrame, item: str, search_kw: str) -> pd.DataFrame:
        pass


class ProductionFilterStrategy(FilterStrategy):
    """품목 선택 및 다중 필드 검색어 필터링 전략"""
    def filter(self, df: pd.DataFrame, item: str, search_kw: str) -> pd.DataFrame:
        filtered = df.copy()

        # 1. 품목 필터링
        if item != "전체" and "item_name" in filtered.columns:
            filtered = filtered[filtered["item_name"] == item]

        # 2. 키워드 통합 검색
        if search_kw.strip():
            kw = search_kw.strip().lower()
            target_cols = ["production_no", "order_no", "item_name", "fg_lot_no"]
            match_mask = pd.Series(False, index=filtered.index)
            
            for col in target_cols:
                if col in filtered.columns:
                    match_mask |= filtered[col].astype(str).str.lower().str.contains(kw)
            
            filtered = filtered[match_mask]

        return filtered


class MetricsStrategy(ABC):
    """KPI 지표 계산 및 바인딩 전략 인터페이스"""
    @abstractmethod
    def render_metrics(self, df: pd.DataFrame) -> None:
        pass


class ProductionMetricsStrategy(MetricsStrategy):
    """생산실적 메트릭 수집 및 렌더링 전략"""
    def render_metrics(self, df: pd.DataFrame) -> None:
        if "good_qty" in df.columns:
            good = pd.to_numeric(df["good_qty"], errors="coerce").fillna(0).sum()
        else:
            good = 0.0

        if "defect_qty" in df.columns:
            defect = pd.to_numeric(df["defect_qty"], errors="coerce").fillna(0).sum()
        else:
            defect = 0.0

        total_prod = good + defect
        avg_yield = (good / total_prod * 100) if total_prod > 0 else 0.0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("총 생산실적 건수", f"{len(df)} 건")
        m2.metric("누적 양품 수량", f"{good:,.0f} EA")
        m3.metric("누적 불량 수량", f"{defect:,.0f} EA")
        m4.metric("평균 수율", f"{avg_yield:.1f} %")


# ==========================================
# 2. UI Helpers & Context Runner
# ==========================================

def safe_page_title(title: str, icon: str, category: str, desc: str) -> None:
    """UI 모듈 호출 시 인자 타입 안전 보장"""
    try:
        from src.ui import page_title
        page_title(title, icon, category, desc)
    except Exception:
        st.title(f"{icon} {title}")
        st.caption(desc)


def safe_show_dataframe(df: pd.DataFrame) -> None:
    """DataFrame 출력 래퍼"""
    try:
        from src.ui import show_dataframe
        show_dataframe(df, "조건에 해당하는 생산실적이 없습니다.")
    except Exception:
        if df.empty:
            st.info("조건에 해당하는 생산실적이 없습니다.")
        else:
            st.dataframe(df, use_container_width=True)


class ProductionPageContext:
    """전략(Strategy) 객체들을 결합하고 실행 흐름을 조율하는 컨텍스트 클래스"""
    def __init__(
        self,
        fetcher: DataFetcherStrategy,
        filterer: FilterStrategy,
        metrics: MetricsStrategy
    ):
        self.fetcher = fetcher
        self.filterer = filterer
        self.metrics = metrics

    def run(self) -> None:
        safe_page_title(
            "생산실적 조회", "🏭", "생산 관리",
            "생산번호, 품목명, 완제품 LOT 번호를 검색하고 생산수량을 확인합니다."
        )

        if not DB_PATH.exists():
            st.warning("DB 파일이 존재하지 않아 초기화합니다.")
            initialize_database()

        # 1. 데이터 로드 및 메트릭 출력
        df = self.fetcher.fetch()
        self.metrics.render_metrics(df)

        st.markdown("---")

        # 2. 사용자 필터 컨트롤
        f1, f2 = st.columns([1, 2])
        items = ["전체"] + (list(df["item_name"].dropna().unique()) if "item_name" in df.columns else [])
        selected_item = f1.selectbox("품목 선택", options=items)
        search_kw = f2.text_input("검색어 (생산번호 / 작업지시번호 / 품목명 / 완제품 LOT)", placeholder="검색어를 입력하세요...")

        # 3. 데이터 필터링 및 테이블 출력
        filtered_df = self.filterer.filter(df, selected_item, search_kw)
        st.subheader(f"조회 결과 ({len(filtered_df)}건)")
        safe_show_dataframe(filtered_df)


# ==========================================
# 3. Page Main Execution
# ==========================================

try:
    context = ProductionPageContext(
        fetcher=ProductionQueryStrategy([
            "productions", "get_productions", "get_production_history",
            "production_history", "production_list"
        ]),
        filterer=ProductionFilterStrategy(),
        metrics=ProductionMetricsStrategy()
    )
    context.run()
except Exception as exc:
    st.error("생산실적 페이지를 로드하는 중 오류가 발생했습니다.")
    st.exception(exc)