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


class RmLotFetcherStrategy(ABC):
    """원자재 LOT 목록 조회 전략 인터페이스"""
    @abstractmethod
    def fetch_rm_lots(self) -> pd.DataFrame:
        pass


class ForwardTraceStrategy(ABC):
    """정방향 추적 실행 전략 인터페이스"""
    @abstractmethod
    def trace(self, target_rm_lot: str) -> dict:
        pass


class TraceMetricsStrategy(ABC):
    """추적 결과 지표 렌더링 전략 인터페이스"""
    @abstractmethod
    def render_metrics(self, trace_result: dict) -> None:
        pass


class DefaultRmLotFetcherStrategy(RmLotFetcherStrategy):
    """queries 모듈에서 원자재 LOT 데이터를 안전하게 탐색하는 전략"""
    def fetch_rm_lots(self) -> pd.DataFrame:
        for query_name in ["lots", "get_lots", "inventory_lots", "get_inventory_lots", "raw_material_lots"]:
            if hasattr(queries, query_name):
                try:
                    res = getattr(queries, query_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        if "lot_type" in res.columns:
                            rm_df = res[res["lot_type"].astype(str).str.contains("원자재|원료|RM|MATERIAL", case=False, na=False)]
                            if not rm_df.empty:
                                return rm_df
                        return res
                except Exception:
                    continue
        return pd.DataFrame(columns=["lot_no", "item_code", "item_name", "qty", "status"])


class DefaultForwardTraceStrategy(ForwardTraceStrategy):
    """원자재 LOT 기준으로 완제품 및 출하 내역을 정방향 추적하는 전략"""
    def trace(self, target_rm_lot: str) -> dict:
        result = {
            "rm_lot": target_rm_lot,
            "productions": pd.DataFrame(),
            "shipments": pd.DataFrame()
        }
        
        if not target_rm_lot:
            return result

        # 1. 전용 쿼리 함수 존재 여부 확인
        for query_name in ["forward_trace", "get_forward_trace", "trace_forward"]:
            if hasattr(queries, query_name):
                try:
                    fn = getattr(queries, query_name)
                    res = fn(target_rm_lot)
                    if isinstance(res, dict):
                        return res
                except Exception:
                    continue

        # 2. 생산 실적 기반 폴백 추적
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
            # rm_lots 또는 rm_lot_no 컬럼에서 매칭되는 완제품 생산 찾기
            mask = pd.Series(False, index=prods_df.index)
            for col in ["rm_lots", "rm_lot_no", "raw_material_lot", "lot_no"]:
                if col in prods_df.columns:
                    mask |= prods_df[col].astype(str).str.contains(target_rm_lot, case=False, na=False)
            
            matched_prods = prods_df[mask] if mask.any() else prods_df.head(0)
            result["productions"] = matched_prods

            # 완제품 LOT 기반 출하 정보 추적
            if not matched_prods.empty and "fg_lot_no" in matched_prods.columns:
                fg_lots = matched_prods["fg_lot_no"].dropna().unique()
                shipments_df = pd.DataFrame()
                
                for sq_name in ["shipments", "get_shipments", "shipment_history"]:
                    if hasattr(queries, sq_name):
                        try:
                            s_res = getattr(queries, sq_name)()
                            if isinstance(s_res, pd.DataFrame) and not s_res.empty:
                                shipments_df = s_res
                                break
                        except Exception:
                            continue

                if not shipments_df.empty:
                    s_mask = pd.Series(False, index=shipments_df.index)
                    for scol in ["fg_lot_no", "lot_no", "item_lot"]:
                        if scol in shipments_df.columns:
                            s_mask |= shipments_df[scol].astype(str).isin(fg_lots)
                    result["shipments"] = shipments_df[s_mask]

        return result


class DefaultTraceMetricsStrategy(TraceMetricsStrategy):
    """정방향 추적 결과 KPI 출력 전략"""
    def render_metrics(self, trace_result: dict) -> None:
        prods = trace_result.get("productions", pd.DataFrame())
        ships = trace_result.get("shipments", pd.DataFrame())

        prod_cnt = len(prods) if isinstance(prods, pd.DataFrame) else 0
        ship_cnt = len(ships) if isinstance(ships, pd.DataFrame) else 0
        
        fg_lot_cnt = 0
        if isinstance(prods, pd.DataFrame) and "fg_lot_no" in prods.columns:
            fg_lot_cnt = prods["fg_lot_no"].nunique()

        total_ship_qty = 0.0
        if isinstance(ships, pd.DataFrame) and not ships.empty:
            for qty_col in ["qty", "shipped_qty", "ship_qty"]:
                if qty_col in ships.columns:
                    total_ship_qty = pd.to_numeric(ships[qty_col], errors="coerce").fillna(0).sum()
                    break

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("선택 원자재 LOT", trace_result.get("rm_lot", "-"))
        m2.metric("투입 완제품 생산 건수", f"{prod_cnt} 건")
        m3.metric("파생 완제품 LOT 수", f"{fg_lot_cnt} 개")
        m4.metric("연관 출하 누적 수량", f"{total_ship_qty:,.0f} EA")


class ForwardTraceContext:
    """정방향 추적 페이지 실행 컨텍스트 클래스"""
    def __init__(
        self,
        lot_fetcher: RmLotFetcherStrategy,
        trace_strategy: ForwardTraceStrategy,
        metrics_strategy: TraceMetricsStrategy
    ):
        self.lot_fetcher = lot_fetcher
        self.trace_strategy = trace_strategy
        self.metrics_strategy = metrics_strategy

    def run(self) -> None:
        page_title(
            "정방향 LOT 추적",
            "🔍",
            "추적 관리",
            "원자재 LOT를 선택하고 영향을 받는 완제품 LOT 및 출하 이력을 확인합니다."
        )

        if not DB_PATH.exists():
            st.warning("DB 파일이 존재하지 않아 초기화합니다.")
            initialize_database()

        rm_lots_df = self.lot_fetcher.fetch_rm_lots()

        if not rm_lots_df.empty and "lot_no" in rm_lots_df.columns:
            lot_options = list(rm_lots_df["lot_no"].astype(str).unique())
        else:
            lot_options = []

        st.subheader("🔎 추적 대상 원자재 LOT 선택")
        c1, c2 = st.columns([2, 1])
        selected_rm_lot = c1.selectbox("원자재 LOT 번호", options=["선택하세요"] + lot_options)
        
        target_lot = selected_rm_lot if selected_rm_lot != "선택하세요" else ""
        
        if target_lot:
            trace_res = self.trace_strategy.trace(target_lot)
            
            st.markdown("---")
            st.subheader("📊 정방향 추적 요약")
            self.metrics_strategy.render_metrics(trace_res)

            st.markdown("---")
            st.subheader("🏭 1차 영향: 생산 실적 및 완제품 (FG) LOT 목록")
            safe_show_dataframe(trace_res.get("productions", pd.DataFrame()), "해당 원자재 LOT가 투입된 생산 실적이 없습니다.")

            st.subheader("🚚 2차 영향: 완제품 출하 내역")
            safe_show_dataframe(trace_res.get("shipments", pd.DataFrame()), "해당 완제품 LOT의 출하 내역이 없습니다.")
        else:
            st.info("상단에서 추적할 원자재 LOT를 선택해주세요.")


try:
    context = ForwardTraceContext(
        lot_fetcher=DefaultRmLotFetcherStrategy(),
        trace_strategy=DefaultForwardTraceStrategy(),
        metrics_strategy=DefaultTraceMetricsStrategy()
    )
    context.run()
except Exception as exc:
    st.error("정방향 추적 페이지를 로드하는 중 오류가 발생했습니다.")
    st.exception(exc)