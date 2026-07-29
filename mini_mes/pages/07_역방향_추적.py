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


class FgLotFetcherStrategy(ABC):
    """완제품(FG) LOT 목록 조회 전략 인터페이스"""
    @abstractmethod
    def fetch_fg_lots(self) -> pd.DataFrame:
        pass


class BackwardTraceStrategy(ABC):
    """역방향 추적 실행 전략 인터페이스"""
    @abstractmethod
    def trace(self, target_fg_lot: str) -> dict:
        pass


class TraceMetricsStrategy(ABC):
    """추적 결과 지표 렌더링 전략 인터페이스"""
    @abstractmethod
    def render_metrics(self, trace_result: dict) -> None:
        pass


class DefaultFgLotFetcherStrategy(FgLotFetcherStrategy):
    """queries 모듈에서 완제품 LOT 데이터를 안전하게 탐색하는 전략"""
    def fetch_fg_lots(self) -> pd.DataFrame:
        # 1. 생산 실적에서 완제품 LOT 추출 시도
        for query_name in ["productions", "get_productions", "production_history"]:
            if hasattr(queries, query_name):
                try:
                    res = getattr(queries, query_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        if "fg_lot_no" in res.columns:
                            return res
                except Exception:
                    continue

        # 2. LOT 관리에서 완제품 LOT 추출 시도
        for query_name in ["lots", "get_lots", "inventory_lots", "get_inventory_lots"]:
            if hasattr(queries, query_name):
                try:
                    res = getattr(queries, query_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        if "lot_type" in res.columns:
                            fg_df = res[res["lot_type"].astype(str).str.contains("완제품|FG|PRODUCT", case=False, na=False)]
                            if not fg_df.empty:
                                return fg_df
                        return res
                except Exception:
                    continue

        return pd.DataFrame(columns=["fg_lot_no", "item_code", "item_name", "good_qty", "production_date"])


class DefaultBackwardTraceStrategy(BackwardTraceStrategy):
    """완제품 LOT 기준으로 투입된 원자재 LOT 및 품질/생산 이력을 역방향 추적하는 전략"""
    def trace(self, target_fg_lot: str) -> dict:
        result = {
            "fg_lot": target_fg_lot,
            "production_info": pd.DataFrame(),
            "rm_lots_info": pd.DataFrame(),
            "quality_inspections": pd.DataFrame()
        }
        
        if not target_fg_lot:
            return result

        # 1. 전용 역방향 쿼리 함수 존재 여부 확인
        for query_name in ["backward_trace", "get_backward_trace", "trace_backward"]:
            if hasattr(queries, query_name):
                try:
                    fn = getattr(queries, query_name)
                    res = fn(target_fg_lot)
                    if isinstance(res, dict):
                        return res
                except Exception:
                    continue

        # 2. 생산 실적 기반 매칭
        prods_df = pd.DataFrame()
        for q_name in ["productions", "get_productions", "production_history", "get_production_history"]:
            if hasattr(queries, q_name):
                try:
                    res = getattr(queries, q_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        prods_df = res
                        break
                except Exception:
                    continue

        if not prods_df.empty:
            mask = pd.Series(False, index=prods_df.index)
            for col in ["fg_lot_no", "lot_no", "production_no"]:
                if col in prods_df.columns:
                    mask |= prods_df[col].astype(str).str.contains(target_fg_lot, case=False, na=False)
            
            matched_prods = prods_df[mask] if mask.any() else prods_df.head(0)
            result["production_info"] = matched_prods

            # 투입 원자재 LOT 추출 및 정보 구성
            rm_lot_list = []
            if not matched_prods.empty:
                for col in ["rm_lots", "rm_lot_no", "raw_material_lot"]:
                    if col in matched_prods.columns:
                        vals = matched_prods[col].dropna().tolist()
                        for val in vals:
                            if isinstance(val, list):
                                rm_lot_list.extend(val)
                            elif isinstance(val, str):
                                rm_lot_list.extend([v.strip() for v in val.split(",") if v.strip()])

            # 전체 LOT 정보에서 투입된 원자재 LOT 매칭
            all_lots = pd.DataFrame()
            for l_name in ["lots", "get_lots", "inventory_lots", "get_inventory_lots"]:
                if hasattr(queries, l_name):
                    try:
                        l_res = getattr(queries, l_name)()
                        if isinstance(l_res, pd.DataFrame) and not l_res.empty:
                            all_lots = l_res
                            break
                    except Exception:
                        continue

            if not all_lots.empty and rm_lot_list:
                l_mask = pd.Series(False, index=all_lots.index)
                if "lot_no" in all_lots.columns:
                    l_mask |= all_lots["lot_no"].astype(str).isin(rm_lot_list)
                result["rm_lots_info"] = all_lots[l_mask]
            elif rm_lot_list:
                result["rm_lots_info"] = pd.DataFrame({"lot_no": rm_lot_list, "lot_type": "원자재"})

        # 3. 품질 검사 내역 추적
        qual_df = pd.DataFrame()
        for qq_name in ["quality_inspections", "get_quality_inspections", "quality", "get_quality"]:
            if hasattr(queries, qq_name):
                try:
                    q_res = getattr(queries, qq_name)()
                    if isinstance(q_res, pd.DataFrame) and not q_res.empty:
                        qual_df = q_res
                        break
                except Exception:
                    continue

        if not qual_df.empty:
            q_mask = pd.Series(False, index=qual_df.index)
            for qcol in ["lot_no", "fg_lot_no", "item_name"]:
                if qcol in qual_df.columns:
                    q_mask |= qual_df[qcol].astype(str).str.contains(target_fg_lot, case=False, na=False)
            result["quality_inspections"] = qual_df[q_mask]

        return result


class DefaultTraceMetricsStrategy(TraceMetricsStrategy):
    """역방향 추적 결과 KPI 출력 전략"""
    def render_metrics(self, trace_result: dict) -> None:
        prods = trace_result.get("production_info", pd.DataFrame())
        rm_lots = trace_result.get("rm_lots_info", pd.DataFrame())
        quals = trace_result.get("quality_inspections", pd.DataFrame())

        good_qty = 0.0
        if isinstance(prods, pd.DataFrame) and not prods.empty:
            if "good_qty" in prods.columns:
                good_qty = pd.to_numeric(prods["good_qty"], errors="coerce").fillna(0).sum()

        rm_cnt = len(rm_lots) if isinstance(rm_lots, pd.DataFrame) else 0
        qual_cnt = len(quals) if isinstance(quals, pd.DataFrame) else 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("선택 완제품 LOT", trace_result.get("fg_lot", "-"))
        m2.metric("생산 양품 수량", f"{good_qty:,.0f} EA")
        m3.metric("투입 원자재 LOT 수", f"{rm_cnt} 개")
        m4.metric("연관 품질 검사 건수", f"{qual_cnt} 건")


class BackwardTraceContext:
    """역방향 추적 페이지 실행 컨텍스트 클래스"""
    def __init__(
        self,
        lot_fetcher: FgLotFetcherStrategy,
        trace_strategy: BackwardTraceStrategy,
        metrics_strategy: TraceMetricsStrategy
    ):
        self.lot_fetcher = lot_fetcher
        self.trace_strategy = trace_strategy
        self.metrics_strategy = metrics_strategy

    def run(self) -> None:
        page_title(
            "역방향 LOT 추적",
            "🔍",
            "추적 관리",
            "완제품 LOT를 선택하고 사용 원자재 LOT와 투입수량을 확인합니다."
        )

        if not DB_PATH.exists():
            st.warning("DB 파일이 존재하지 않아 초기화합니다.")
            initialize_database()

        fg_df = self.lot_fetcher.fetch_fg_lots()

        fg_options = []
        if not fg_df.empty:
            for col in ["fg_lot_no", "lot_no"]:
                if col in fg_df.columns:
                    fg_options = list(fg_df[col].dropna().astype(str).unique())
                    break

        st.subheader("🔎 추적 대상 완제품 (FG) LOT 선택")
        c1, c2 = st.columns([2, 1])
        selected_fg_lot = c1.selectbox("완제품 LOT 번호", options=["선택하세요"] + fg_options)
        
        target_lot = selected_fg_lot if selected_fg_lot != "선택하세요" else ""
        
        if target_lot:
            trace_res = self.trace_strategy.trace(target_lot)
            
            st.markdown("---")
            st.subheader("📊 역방향 추적 요약")
            self.metrics_strategy.render_metrics(trace_res)

            st.markdown("---")
            st.subheader("🏭 1차 근원: 생산 실적 및 작업 정보")
            safe_show_dataframe(trace_res.get("production_info", pd.DataFrame()), "해당 완제품 LOT의 생산 실적이 없습니다.")

            st.subheader("📦 2차 근원: 투입 원자재 (RM) LOT 목록")
            safe_show_dataframe(trace_res.get("rm_lots_info", pd.DataFrame()), "해당 완제품 LOT에 투입된 원자재 LOT 정보가 없습니다.")

            st.subheader("🧪 연관 품질 검사 이력")
            safe_show_dataframe(trace_res.get("quality_inspections", pd.DataFrame()), "해당 완제품 LOT에 대한 품질 검사 이력이 없습니다.")
        else:
            st.info("상단에서 추적할 완제품 LOT를 선택해주세요.")


try:
    context = BackwardTraceContext(
        lot_fetcher=DefaultFgLotFetcherStrategy(),
        trace_strategy=DefaultBackwardTraceStrategy(),
        metrics_strategy=DefaultTraceMetricsStrategy()
    )
    context.run()
except Exception as exc:
    st.error("역방향 추적 페이지를 로드하는 중 오류가 발생했습니다.")
    st.exception(exc)