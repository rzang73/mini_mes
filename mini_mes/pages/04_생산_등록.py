from abc import ABC, abstractmethod
import datetime
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


class OrderFetcherStrategy(ABC):
    """작업지시 데이터 조회 전략 인터페이스"""
    @abstractmethod
    def fetch_orders(self) -> pd.DataFrame:
        pass


class LotFetcherStrategy(ABC):
    """원자재 LOT 데이터 조회 전략 인터페이스"""
    @abstractmethod
    def fetch_raw_material_lots(self) -> pd.DataFrame:
        pass


class SaveProductionStrategy(ABC):
    """생산실적 저장 전략 인터페이스"""
    @abstractmethod
    def save(self, payload: dict) -> bool:
        pass


class DefaultOrderFetcherStrategy(OrderFetcherStrategy):
    """ queries 모듈을 통한 작업지시 목록 조회 전략"""
    def fetch_orders(self) -> pd.DataFrame:
        for query_name in ["orders", "get_orders", "work_orders", "get_work_orders"]:
            if hasattr(queries, query_name):
                try:
                    res = getattr(queries, query_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        return res
                except Exception:
                    continue
        return pd.DataFrame(columns=["order_no", "item_code", "item_name", "order_qty", "status"])


class DefaultLotFetcherStrategy(LotFetcherStrategy):
    """queries 모듈을 통한 원자재 LOT 목록 조회 전략"""
    def fetch_raw_material_lots(self) -> pd.DataFrame:
        for query_name in ["lots", "get_lots", "inventory_lots", "get_inventory_lots"]:
            if hasattr(queries, query_name):
                try:
                    res = getattr(queries, query_name)()
                    if isinstance(res, pd.DataFrame) and not res.empty:
                        # 원자재 LOT 조건 필터링
                        if "lot_type" in res.columns:
                            rm_df = res[res["lot_type"].astype(str).str.contains("원자재|원료|RM|MATERIAL", case=False, na=False)]
                            if not rm_df.empty:
                                return rm_df
                        return res
                except Exception:
                    continue
        return pd.DataFrame(columns=["lot_no", "item_code", "item_name", "qty", "status"])


class DefaultSaveProductionStrategy(SaveProductionStrategy):
    """생산실적 등록 DB 저장 전략"""
    def save(self, payload: dict) -> bool:
        save_funcs = [
            "insert_production", "add_production", "save_production",
            "create_production", "insert_production_result"
        ]
        for fn_name in save_funcs:
            if hasattr(queries, fn_name):
                try:
                    fn = getattr(queries, fn_name)
                    # 키워드 인자 지원 유무 대응
                    try:
                        fn(**payload)
                    except TypeError:
                        fn(payload)
                    return True
                except Exception as e:
                    st.error(f"저장 중 오류가 발생했습니다 ({fn_name}): {e}")
                    return False
        
        # queries 모듈에 적합한 함수가 없을 시 임시 알림
        st.warning("생산실적 저장 전용 DB 함수를 찾지 못했습니다. queries 모듈을 확인해주세요.")
        return False


class ProductionRegistrationContext:
    """생산등록 흐름 조율 컨텍스트 클래스"""
    def __init__(
        self,
        order_fetcher: OrderFetcherStrategy,
        lot_fetcher: LotFetcherStrategy,
        save_strategy: SaveProductionStrategy
    ):
        self.order_fetcher = order_fetcher
        self.lot_fetcher = lot_fetcher
        self.save_strategy = save_strategy

    def run(self) -> None:
        page_title(
            "생산 등록",
            "🏭",
            "생산 관리",
            "생산할 제품과 투입 원자재 LOT를 선택하고 저장 결과를 확인합니다."
        )

        if not DB_PATH.exists():
            st.warning("DB 파일이 존재하지 않아 초기화합니다.")
            initialize_database()

        orders_df = self.order_fetcher.fetch_orders()
        rm_lots_df = self.lot_fetcher.fetch_raw_material_lots()

        st.subheader("📝 생산 실적 등록 작성")

        with st.form("production_registration_form", clear_on_submit=False):
            col1, col2 = st.columns(2)

            with col1:
                # 작업지시 선택 옵션 구성
                if not orders_df.empty and "order_no" in orders_df.columns:
                    order_opts = ["선택 안함"] + list(orders_df["order_no"].astype(str).unique())
                else:
                    order_opts = ["선택 안함"]
                
                selected_order = st.selectbox("작업지시 번호", options=order_opts)

                # 품목명 자동 바인딩 또는 직접 입력
                default_item = ""
                if selected_order != "선택 안함" and not orders_df.empty and "item_name" in orders_df.columns:
                    matched = orders_df[orders_df["order_no"].astype(str) == selected_order]
                    if not matched.empty:
                        default_item = str(matched.iloc[0]["item_name"])

                item_name = st.text_input("품목명", value=default_item, placeholder="품목명을 입력하거나 작업지시를 선택하세요")
                fg_lot_no = st.text_input("완제품 LOT 번호", placeholder="예: LOT-FG-20260728-001")

            with col2:
                good_qty = st.number_input("양품 수량 (EA)", min_value=0, value=1000, step=100)
                defect_qty = st.number_input("불량 수량 (EA)", min_value=0, value=0, step=10)
                prod_date = st.date_input("생산 일자", value=datetime.date.today())

            # 원자재 LOT 투입 선택
            st.markdown("**투입 원자재 LOT 선택**")
            if not rm_lots_df.empty and "lot_no" in rm_lots_df.columns:
                available_rm_lots = list(rm_lots_df["lot_no"].astype(str).unique())
            else:
                available_rm_lots = []

            selected_rm_lots = st.multiselect(
                "투입 원자재 LOT 목록",
                options=available_rm_lots,
                placeholder="투입된 원자재 LOT를 선택하세요"
            )

            submit_btn = st.form_submit_button("💾 생산실적 등록 및 저장", use_container_width=True)

        if submit_btn:
            if not item_name.strip():
                st.error("품목명을 입력해 주세요.")
                return

            total_input = good_qty + defect_qty
            yield_rate = (good_qty / total_input * 100.0) if total_input > 0 else 0.0

            payload = {
                "order_no": selected_order if selected_order != "선택 안함" else "",
                "item_name": item_name.strip(),
                "fg_lot_no": fg_lot_no.strip(),
                "good_qty": good_qty,
                "defect_qty": defect_qty,
                "yield_rate": round(yield_rate, 2),
                "production_date": str(prod_date),
                "rm_lots": selected_rm_lots
            }

            if self.save_strategy.save(payload):
                st.success(f"생산실적 등록 성공! (양품: {good_qty:,} EA, 수율: {yield_rate:.1f}%)")
                st.balloons()

        st.markdown("---")
        st.subheader("📋 진행 가능 작업지시 목록")
        safe_show_dataframe(orders_df, "진행 가능한 작업지시 데이터가 없습니다.")


try:
    context = ProductionRegistrationContext(
        order_fetcher=DefaultOrderFetcherStrategy(),
        lot_fetcher=DefaultLotFetcherStrategy(),
        save_strategy=DefaultSaveProductionStrategy()
    )
    context.run()
except Exception as exc:
    st.error("생산 등록 페이지를 로드하는 중 오류가 발생했습니다.")
    st.exception(exc)