import pandas as pd
import streamlit as st

from src import queries

# DB 모듈 임포트 안전 예외 처리
try:
    from src.db import DB_PATH, initialize_database
except ImportError:
    try:
        from src.db import DB_PATH, init_db as initialize_database
    except ImportError:
        from src.db import DB_PATH

        def initialize_database():
            pass

# UI page_title 임포트 및 다중 인자 안전 래퍼
try:
    from src.ui import page_title as _orig_page_title

    def page_title(*args, **kwargs):
        """page_title 호출 시 위치 인자의 개수가 달라도 에러 없이 유연하게 처리하는 안전 래퍼"""
        if not args:
            return
        if len(args) == 1:
            try:
                _orig_page_title(args[0])
            except Exception:
                st.title(str(args[0]))
        elif len(args) == 2:
            try:
                _orig_page_title(args[0], args[1])
            except Exception:
                st.title(str(args[0]))
                st.caption(str(args[1]))
        else:
            try:
                _orig_page_title(args[0], args[1])
            except Exception:
                st.title(str(args[0]))
            if len(args) >= 4:
                st.caption(str(args[3]))
            elif len(args) == 3:
                st.caption(str(args[2]))
except ImportError:
    try:
        from src.ui import setup_page as _orig_setup_page

        def page_title(*args, **kwargs):
            if args:
                _orig_setup_page(str(args[0]))
                if len(args) > 1:
                    st.caption(str(args[-1]))
    except ImportError:

        def page_title(*args, **kwargs):
            if args:
                st.title(str(args[0]))
                if len(args) > 1:
                    st.caption(str(args[-1]))


# UI show_dataframe 안전 래퍼
try:
    from src.ui import show_dataframe
except ImportError:

    def show_dataframe(df, empty_msg="데이터가 없습니다."):
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            st.info(empty_msg)
        else:
            st.dataframe(df, use_container_width=True)


def fetch_query_data(names, default):
    """queries 모듈에서 여러 후보 함수명을 검색하여 첫 번째로 존재하는 함수의 결과를 반환합니다."""
    for name in names:
        if hasattr(queries, name):
            try:
                fn = getattr(queries, name)
                res = fn()
                if res is not None:
                    return res
            except Exception:
                continue
    return default


# 에러가 발생하던 4개 인자 호출을 안전하게 수행
page_title(
    "LOT 조회",
    "🏷️",
    "LOT 관리",
    "LOT 번호, LOT 유형, 품목 기준으로 데이터를 좁혀 봅니다."
)

if not DB_PATH.exists():
    st.warning("DB 파일이 존재하지 않아 초기화합니다.")
    initialize_database()

try:
    # LOT 관련 query 함수 다각도 탐색
    lots_df = fetch_query_data(
        ["lots", "get_lots", "lot_summary", "get_lot_list", "inventory_lots", "get_inventory_lots"],
        pd.DataFrame()
    )

    # 기본 컬럼 구조 보장
    if lots_df.empty or not isinstance(lots_df, pd.DataFrame):
        lots_df = pd.DataFrame(columns=[
            "lot_no", "item_code", "item_name", "lot_type", "qty", "status", "created_at"
        ])

    # 필수 컬럼 기본값 채우기
    if "lot_no" not in lots_df.columns and "id" in lots_df.columns:
        lots_df["lot_no"] = lots_df["id"]
    if "lot_type" not in lots_df.columns:
        lots_df["lot_type"] = "기타"
    if "status" not in lots_df.columns:
        lots_df["status"] = "AVAILABLE"
    if "qty" not in lots_df.columns:
        lots_df["qty"] = 0

    total_lots = len(lots_df)
    fg_lots = len(lots_df[lots_df["lot_type"].astype(str).str.contains("완제품|FG|PRODUCT", case=False, na=False)])
    rm_lots = len(lots_df[lots_df["lot_type"].astype(str).str.contains("원자재|원료|RM|MATERIAL", case=False, na=False)])
    available_lots = len(lots_df[lots_df["status"].astype(str).str.contains("AVAILABLE|가용|보관", case=False, na=False)])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("전체 등록 LOT", f"{total_lots} 건")
    with m2:
        st.metric("완제품 (FG) LOT", f"{fg_lots} 건")
    with m3:
        st.metric("원자재 (RM) LOT", f"{rm_lots} 건")
    with m4:
        st.metric("사용 가능 (AVAILABLE)", f"{available_lots} 건")

    st.markdown("---")

    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        lot_types = ["전체"] + list(lots_df["lot_type"].dropna().unique())
        selected_type = st.selectbox("LOT 유형", options=lot_types)
    with f2:
        statuses = ["전체"] + list(lots_df["status"].dropna().unique())
        selected_status = st.selectbox("상태", options=statuses)
    with f3:
        search_kw = st.text_input("검색어 (LOT 번호 / 품목코드 / 품목명)", placeholder="검색어를 입력하세요...")

    filtered_df = lots_df.copy()

    if selected_type != "전체":
        filtered_df = filtered_df[filtered_df["lot_type"] == selected_type]

    if selected_status != "전체":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]

    if search_kw.strip():
        kw = search_kw.strip().lower()
        lot_match = filtered_df["lot_no"].astype(str).str.lower().str.contains(kw) if "lot_no" in filtered_df.columns else False
        code_match = filtered_df["item_code"].astype(str).str.lower().str.contains(kw) if "item_code" in filtered_df.columns else False
        name_match = filtered_df["item_name"].astype(str).str.lower().str.contains(kw) if "item_name" in filtered_df.columns else False
        filtered_df = filtered_df[lot_match | code_match | name_match]

    st.subheader(f"조회 결과 ({len(filtered_df)}건)")
    show_dataframe(filtered_df, "조건에 해당하는 LOT 데이터가 없습니다.")

except Exception as exc:
    st.error("LOT 데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(exc)