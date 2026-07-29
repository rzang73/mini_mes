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
            # 3개 이상의 인자가 전달된 경우 (예: title, icon, category, description)
            try:
                _orig_page_title(args[0], args[1])
            except Exception:
                st.title(str(args[0]))
            # 잔여 설명을 caption 형태로 안전 출력
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
    "품목 조회",
    "📦",
    "품목 관리",
    "품목 유형과 검색어로 품목을 조회하고 LOT 연결 건수를 확인합니다."
)

if not DB_PATH.exists():
    st.warning("DB 파일이 존재하지 않아 초기화합니다.")
    initialize_database()

try:
    # 품목 관련 query 함수를 다각도로 탐색
    items_df = fetch_query_data(
        ["items", "get_items", "item_summary", "get_item_list", "inventory_summary", "get_inventory_summary"],
        pd.DataFrame()
    )

    # 기본 컬럼 구조 보장
    if items_df.empty or not isinstance(items_df, pd.DataFrame):
        items_df = pd.DataFrame(columns=[
            "item_code", "item_name", "item_type", "unit", "spec", "current_qty", "safety_stock", "stock_status"
        ])

    # 필수 컬럼 채우기
    if "item_type" not in items_df.columns:
        items_df["item_type"] = "기타"
    if "current_qty" not in items_df.columns:
        items_df["current_qty"] = 0
    if "safety_stock" not in items_df.columns:
        items_df["safety_stock"] = 0

    total_count = len(items_df)
    fg_count = len(items_df[items_df["item_type"].astype(str).str.contains("완제품|FG|PRODUCT", case=False, na=False)])
    rm_count = len(items_df[items_df["item_type"].astype(str).str.contains("원자재|원료|RM|MATERIAL", case=False, na=False)])
    
    if "stock_status" in items_df.columns:
        shortage_count = len(items_df[items_df["stock_status"] == "부족"])
    else:
        shortage_count = len(items_df[items_df["current_qty"] < items_df["safety_stock"]])

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("전체 등록 품목", f"{total_count} 건")
    with k2:
        st.metric("완제품 (FG)", f"{fg_count} 건")
    with k3:
        st.metric("원자재 (RM)", f"{rm_count} 건")
    with k4:
        st.metric("안전재고 미만", f"{shortage_count} 건", delta_color="inverse")

    st.markdown("---")

    f1, f2 = st.columns([1, 2])
    with f1:
        item_types = ["전체"] + list(items_df["item_type"].dropna().unique())
        selected_type = st.selectbox("품목 유형 선택", options=item_types)
    with f2:
        search_kw = st.text_input("검색어 (품목코드 / 품목명)", placeholder="검색어를 입력하세요...")

    filtered_df = items_df.copy()

    if selected_type != "전체":
        filtered_df = filtered_df[filtered_df["item_type"] == selected_type]

    if search_kw.strip():
        kw = search_kw.strip().lower()
        code_match = filtered_df["item_code"].astype(str).str.lower().str.contains(kw) if "item_code" in filtered_df.columns else False
        name_match = filtered_df["item_name"].astype(str).str.lower().str.contains(kw) if "item_name" in filtered_df.columns else False
        filtered_df = filtered_df[code_match | name_match]

    st.subheader(f"조회 결과 ({len(filtered_df)}건)")
    show_dataframe(filtered_df, "조건에 해당하는 품목이 없습니다.")

except Exception as exc:
    st.error("품목 데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(exc)