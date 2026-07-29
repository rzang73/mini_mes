from abc import ABC, abstractmethod
import pandas as pd
import streamlit as st

from src import queries

try:
    from src.db import DB_PATH, initialize_database
except ImportError:
    try:
        from src.db import DB_PATH, init_db as initialize_database
    except ImportError:
        from src.db import DB_PATH

        def initialize_database():
            pass


def page_title(*args, **kwargs):
    """src.ui.page_title 인자 개수 차이로 인한 TypeError 방지 가변 인자 래퍼"""
    if not args:
        return
    
    title = str(args[0])
    icon = str(args[1]) if len(args) > 1 else ""
    category = str(args[2]) if len(args) > 2 else ""
    desc = str(args[3]) if len(args) > 3 else ""

    try:
        from src.ui import page_title as _ui_page_title
        try:
            _ui_page_title(title, icon)
        except TypeError:
            _ui_page_title(title)
    except Exception:
        st.title(f"{icon} {title}".strip())
        if desc:
            st.caption(f"[{category}] {desc}" if category else desc)


def safe_show_dataframe(df: pd.DataFrame, empty_msg: str = "데이터가 없습니다.") -> None:
    """DataFrame 출력 안전 래퍼"""
    try:
        from src.ui import show_dataframe
        show_dataframe(df, empty_msg)
    except Exception:
        if df is None or df.empty:
            st.info(empty_msg)
        else:
            st.dataframe(df, use_container_width=True)


class ProductionDataFetcherStrategy(ABC):
    """생산 현황 데이터 조회 전략 인터페이스"""
    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        pass


class ProductionMetricsStrategy(ABC):
    """생산 현황 KPI 렌더링 전략 인터페이스"""
    @abstractmethod
    def render_metrics(self, df: pd.DataFrame) -> None:
        pass


class ProductionChartStrategy(ABC):
    """생산 시각화 차트 렌더링 전략 인터페이스"""
    @abstractmethod
    def render_charts(self, df: pd.DataFrame) -> None:
        pass


class DefaultProductionDataFetcherStrategy(ProductionDataFetcherStrategy):
    """queries 모듈에서 생산 실적 데이터를 탐색하여 로드하는 전략"""
    def fetch_data(self) -> pd.DataFrame:
        for q_name in ["productions", "get_productions", "production_history", "get_production_history"]:
            if hasattr(queries, q_name):
                try:
                    res = getattr(queries, q_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        return res
                except Exception:
                    continue

        return pd.DataFrame(columns=[
            "production_no", "order_no", "item_code", "item_name",
            "fg_lot_no", "good_qty", "defect_qty", "yield_rate", "production_date"
        ])


class DefaultProductionMetricsStrategy(ProductionMetricsStrategy):
    """생산 현황 요약 KPI 지표 렌더링 전략"""
    def render_metrics(self, df: pd.DataFrame) -> None:
        if df.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("총 생산 건수", "0 건")
            m2.metric("총 양품 수량", "0 EA")
            m3.metric("총 불량 수량", "0 EA")
            m4.metric("평균 수율", "0.0 %")
            return

        total_cnt = len(df)
        good_qty = (
            pd.to_numeric(df["good_qty"], errors="coerce").fillna(0).sum()
            if "good_qty" in df.columns
            else 0.0
        )
        defect_qty = (
            pd.to_numeric(df["defect_qty"], errors="coerce").fillna(0).sum()
            if "defect_qty" in df.columns
            else 0.0
        )
        
        total_qty = good_qty + defect_qty
        avg_yield = (good_qty / total_qty * 100) if total_qty > 0 else 0.0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("총 생산 건수", f"{total_cnt:,} 건")
        m2.metric("총 양품 수량", f"{good_qty:,.0f} EA")
        m3.metric("총 불량 수량", f"{defect_qty:,.0f} EA")
        m4.metric("평균 수율", f"{avg_yield:.1f} %")


class DefaultProductionChartStrategy(ProductionChartStrategy):
    """Streamlit 차트를 이용한 생산 집계 시각화 전략"""
    def render_charts(self, df: pd.DataFrame) -> None:
        if df.empty:
            st.info("시각화할 생산 데이터가 없습니다.")
            return

        c1, c2 = st.columns(2)

        # 1. 품목별 양품 생산 수량 차트
        with c1:
            st.markdown("#### 📦 품목별 생산 양품 수량")
            if "item_name" in df.columns and "good_qty" in df.columns:
                by_item = df.groupby("item_name")["good_qty"].sum().reset_index()
                st.bar_chart(by_item.set_index("item_name"))
            else:
                st.caption("품목별 데이터 집계가 불가능합니다.")

        # 2. 일자별 생산 수량 추이 차트
        with c2:
            st.markdown("#### 📅 일자별 생산 수량 추이")
            if "production_date" in df.columns and "good_qty" in df.columns:
                by_date = df.groupby("production_date")[["good_qty", "defect_qty"]].sum().reset_index()
                st.line_chart(by_date.set_index("production_date"))
            else:
                st.caption("일자별 데이터 집계가 불가능합니다.")


class ProductionStatusContext:
    """생산현황 대시보드 실행 컨텍스트 클래스"""
    def __init__(
        self,
        fetcher: ProductionDataFetcherStrategy,
        metrics: ProductionMetricsStrategy,
        charts: ProductionChartStrategy
    ):
        self.fetcher = fetcher
        self.metrics = metrics
        self.charts = charts

    def run(self) -> None:
        # 안전한 가변 인자 지원 page_title 호출
        page_title(
            "생산현황 대시보드",
            "📊",
            "생산 관리",
            "집계 결과를 표와 간단한 차트로 확인합니다."
        )

        if not DB_PATH.exists():
            st.warning("DB 파일이 존재하지 않아 초기화합니다.")
            initialize_database()

        df = self.fetcher.fetch_data()

        st.subheader("📈 주요 생산 지표 요약")
        self.metrics.render_metrics(df)

        st.markdown("---")
        st.subheader("📊 생산 현황 차트 분석")
        self.charts.render_charts(df)

        st.markdown("---")
        st.subheader("📋 전체 생산 실적 목록")
        safe_show_dataframe(df, "등록된 생산 실적 데이터가 없습니다.")


try:
    context = ProductionStatusContext(
        fetcher=DefaultProductionDataFetcherStrategy(),
        metrics=DefaultProductionMetricsStrategy(),
        charts=DefaultProductionChartStrategy()
    )
    context.run()
except Exception as exc:
    st.error("생산현황 페이지를 로드하는 중 오류가 발생했습니다.")
    st.exception(exc)