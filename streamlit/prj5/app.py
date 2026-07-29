
import streamlit as st
import pandas as pd

# ==========================================
# 0. 웹 브라우저 탭 및 기본 설정
# ==========================================
st.set_page_config(page_title="회사 소개 & 비즈니스 대시보드", layout="wide")

# ==========================================
# 1. 텍스트 레이아웃 및 이미지 섹션
# ==========================================
# 좌우 화면 분할 (텍스트와 이미지를 나란히 배치)
col1, col2 = st.columns([1.5, 1])

with col1:
    st.title('🏢 회사소개')
    st.header('📦 제품소개')
    st.subheader('💡 AI 사업부')
    
    items = ['PLC', 'MES', 'SCADA']
    st.write("보유 제품군 리스트: ", items)

with col2:
    st.write("")  # 레이아웃 정렬용 공백
    # 임시 샘플 공장 스마트팩토리 이미지 연동 (원하는 이미지 파일 경로로 대체 가능)
    sample_image_url = "https://unsplash.com"
    st.image(sample_image_url, caption="스마트팩토리 AI 시스템 예시", use_container_width=True)

# ==========================================
# 2. 마크다운 양식 및 구조화 리스트
# ==========================================
st.markdown('---')  # 화면 구분선
st.markdown('# #️⃣ 주요 구축 시스템')
st.markdown('**스마트팩토리 핵심 요소**')
st.markdown("""
- **MES** (제조실행시스템)
- **PLC** (제조장치 제어기)
- **SCADA** (원격 감시 제어 및 데이터 수집)
""")

# ==========================================
# 3. 데이터 연산 및 핵심 지표(Metric) 대시보드
# ==========================================
st.markdown('---')
st.markdown('# 📊 비즈니스 매출 대시보드')

a = 3500
b = 4500
total_sales = a + b

# 대시보드 상단 요약 지표 위젯 배치
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="상반기 매출 (A)", value=f"{a:,} 만원")
with metric_col2:
    st.metric(label="하반기 매출 (B)", value=f"{b:,} 만원", delta="+1,000 만원")
with metric_col3:
    st.metric(label="총 연간 매출 (A + B)", value=f"{total_sales:,} 만원", delta_color="normal")

# ==========================================
# 4. 대시보드 차트 시각화 섹션
# ==========================================
# 차트를 나란히 배치하기 위한 컬럼 분할
chart_col1, chart_col2 = st.columns(2)

# 시각화용 데이터프레임 빌드
chart_data = pd.DataFrame({
    '시기': ['상반기 (A)', '하반기 (B)'],
    '매출': [a, b]
})

with chart_col1:
    st.subheader("📈 반기별 매출 비교 (바 차트)")
    # 스트림릿 내장 바 차트로 매출 시각화
    st.bar_chart(data=chart_data, x='시기', y='매출', color="#4ECDC4")

with chart_col2:
    st.subheader("📑 제품군별 매출 기여도 예측 (라인 차트)")
    # 흐름 변화를 보여주기 위한 가상 제품군 시뮬레이션 라인 데이터
    trend_data = pd.DataFrame({
        'PLC 매출': [1000, 1200, 1500, a//3],
        'MES 매출': [800, 1100, 1300, b//2],
        'SCADA 매출': [900, 1000, 1100, a//4]
    })
    st.line_chart(trend_data)

import streamlit as st
import pandas as pd

# ==========================================
# 0. 웹 브라우저 탭 및 기본 설정
# ==========================================
st.set_page_config(page_title="회사 소개 & 비즈니스 대시보드", layout="wide")

# ==========================================
# 1. 회사 및 사업부 기본 소개
# ==========================================
st.title('🏢 회사소개')
st.header('📦 제품소개')
st.subheader('💡 AI 사업부')

items = ['PLC', 'MES', 'SCADA']
st.write("보유 제품군 리스트: ", items)

# ==========================================
# 2. 마크다운 주요 구축 시스템 정보
# ==========================================
st.markdown('---')  # 화면 구분선
st.markdown('# #️⃣ 주요 구축 시스템')
st.markdown('**스마트팩토리 핵심 요소**')
st.markdown("""
- **MES** (제조실행시스템)
- **PLC** (제조장치 제어기)
- **SCADA** (원격 감시 제어 및 데이터 수집)
""")

# ==========================================
# 3. 데이터 연산 및 핵심 지표(Metric) 대시보드
# ==========================================
st.markdown('---')
st.markdown('# 📊 비즈니스 매출 대시보드')

a = 3500
b = 4500
total_sales = a + b

# 대시보드 상단 요약 지표 위젯 배치 (3칸 가로 배치)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="상반기 매출 (A)", value=f"{a:,} 만원")
with metric_col2:
    st.metric(label="하반기 매출 (B)", value=f"{b:,} 만원", delta="+1,000 만원")
with metric_col3:
    st.metric(label="총 연간 매출 (A + B)", value=f"{total_sales:,} 만원")

st.markdown('---')

# ==========================================
# 4. [첫 번째 위치] 반기별 매출 비교 (바 차트)
# ==========================================
st.subheader("📈 반기별 매출 비교 (바 차트)")

# 바 차트용 데이터프레임 빌드
bar_chart_data = pd.DataFrame({
    '시기': ['상반기 (A)', '하반기 (B)'],
    '매출': [a, b]
})

# 바 차트 출력
st.bar_chart(data=bar_chart_data, x='시기', y='매출', color="#4ECDC4")

st.markdown('---')

# ==========================================
# 5. [두 번째 위치 - 맨 밑으로 이동] 제품군별 매출 기여도 예측 (라인 차트)
# ==========================================
st.subheader("📑 제품군별 매출 기여도 예측 (라인 차트)")

# 라인 차트용 시뮬레이션 데이터 빌드
trend_data = pd.DataFrame({
    'PLC 매출': [1000, 1200, 1500, a//3],
    'MES 매출': [800, 1100, 1300, b//2],
    'SCADA 매출': [900, 1000, 1100, a//4]
})

# 라인 차트 출력 (화면 맨 아래에 배치)
st.line_chart(trend_data)

import streamlit as st
import pandas as pd

# ==========================================
# 0. 웹 브라우저 탭 및 기본 설정
# ==========================================
st.set_page_config(page_title="회사 소개 & 비즈니스 대시보드", layout="wide")

# ==========================================
# 1. 회사 및 사업부 기본 소개
# ==========================================
st.title('🏢 회사소개')
st.header('📦 제품소개')
st.subheader('💡 AI 사업부')

items = ['PLC', 'MES', 'SCADA']
st.write("보유 제품군 리스트: ", items)

# ==========================================
# 2. 마크다운 주요 구축 시스템 정보
# ==========================================
st.markdown('---')  # 화면 구분선
st.markdown('# #️⃣ 주요 구축 시스템')
st.markdown('**스마트팩토리 핵심 요소**')
st.markdown("""
- **MES** (제조실행시스템)
- **PLC** (제조장치 제어기)
- **SCADA** (원격 감시 제어 및 데이터 수집)
""")

# ==========================================
# 3. 데이터 연산 및 핵심 지표(Metric) 대시보드
# ==========================================
st.markdown('---')
st.markdown('# 📊 비즈니스 매출 대시보드')

a = 3500
b = 4500
total_sales = a + b

# 대시보드 상단 요약 지표 위젯 배치 (3칸 가로 배치)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="상반기 매출 (A)", value=f"{a:,} 만원")
with metric_col2:
    st.metric(label="하반기 매출 (B)", value=f"{b:,} 만원", delta="+1,000 만원")
with metric_col3:
    st.metric(label="총 연간 매출 (A + B)", value=f"{total_sales:,} 만원")

st.markdown('---')

# ==========================================
# 4. 반기별 매출 비교 (바 차트) - [크기 절반 조절]
# ==========================================
# 1:1 비율로 화면을 이등분하여 왼쪽 칸에만 차트를 넣음으로써 크기를 절반으로 줄입니다.
bar_col1, bar_col2 = st.columns([1, 1])

with bar_col1:
    st.subheader("📈 반기별 매출 비교 (바 차트)")

    # 바 차트용 데이터프레임 빌드
    bar_chart_data = pd.DataFrame({
        '시기': ['상반기 (A)', '하반기 (B)'],
        '매출': [a, b]
    })

    # 바 차트 출력
    st.bar_chart(data=bar_chart_data, x='시기', y='매출', color="#4ECDC4")

st.markdown('---')

# ==========================================
# 5. 제품군별 매출 기여도 예측 (라인 차트) - [크기 절반 조절]
# ==========================================
# 마찬가지로 1:1 비율로 분할하여 왼쪽 칸에만 차트를 배치합니다.
line_col1, line_col2 = st.columns([1, 1])

with line_col1:
    st.subheader("📑 제품군별 매출 기여도 예측 (라인 차트)")

    # 라인 차트용 시뮬레이션 데이터 빌드
    trend_data = pd.DataFrame({
        'PLC 매출': [1000, 1200, 1500, a//3],
        'MES 매출': [800, 1100, 1300, b//2],
        'SCADA 매출': [900, 1000, 1100, a//4]
    })

    # 라인 차트 출력
    st.line_chart(trend_data)

import streamlit as st
import pandas as pd

# ==========================================
# 0. 웹 브라우저 탭 및 기본 설정
# ==========================================
st.set_page_config(page_title="회사 소개 & 비즈니스 대시보드", layout="wide")

# ==========================================
# 1. 회사 및 사업부 기본 소개
# ==========================================
st.title('🏢 회사소개')
st.header('📦 제품소개')
st.subheader('💡 AI 사업부')

items = ['PLC', 'MES', 'SCADA']
st.write("보유 제품군 리스트: ", items)

# ==========================================
# 2. 마크다운 주요 구축 시스템 정보
# ==========================================
st.markdown('---')  # 화면 구분선
st.markdown('# #️⃣ 주요 구축 시스템')
st.markdown('**스마트팩토리 핵심 요소**')
st.markdown("""
- **MES** (제조실행시스템)
- **PLC** (제조장치 제어기)
- **SCADA** (원격 감시 제어 및 데이터 수집)
""")

# ==========================================
# 3. 데이터 연산 및 핵심 지표(Metric) 대시보드
# ==========================================
st.markdown('---')
st.markdown('# 📊 비즈니스 매출 대시보드')

a = 3500
b = 4500
total_sales = a + b

# 대시보드 상단 요약 지표 위젯 배치 (3칸 가로 배치)
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="상반기 매출 (A)", value=f"{a:,} 만원")
with metric_col2:
    st.metric(label="하반기 매출 (B)", value=f"{b:,} 만원", delta="+1,000 만원")
with metric_col3:
    st.metric(label="총 연간 매출 (A + B)", value=f"{total_sales:,} 만원")

st.markdown('---')

# ==========================================
# 4. 반기별 매출 비교 (바 차트) - [가운데 정렬]
# ==========================================
# [1, 2, 1] 비율로 컬럼을 나누어 가운데(2 비율 = 전체의 50% 폭)에 배치하여 가운데 정렬 구현
bar_side1, bar_center, bar_side2 = st.columns([1, 2, 1])

with bar_center:
    st.subheader("📈 반기별 매출 비교 (바 차트)")

    # 바 차트용 데이터프레임 빌드
    bar_chart_data = pd.DataFrame({
        '시기': ['상반기 (A)', '하반기 (B)'],
        '매출': [a, b]
    })

    # 바 차트 출력
    st.bar_chart(data=bar_chart_data, x='시기', y='매출', color="#4ECDC4")

st.markdown('---')

# ==========================================
# 5. 제품군별 매출 기여도 예측 (라인 차트) - [가운데 정렬]
# ==========================================
# 마찬가지로 동일한 [1, 2, 1] 비율 구성을 사용하여 정확히 중앙 수직 정렬을 맞춥니다.
line_side1, line_center, line_side2 = st.columns([1, 2, 1])

with line_center:
    st.subheader("📑 제품군별 매출 기여도 예측 (라인 차트)")

    # 라인 차트용 시뮬레이션 데이터 빌드
    trend_data = pd.DataFrame({
        'PLC 매출': [1000, 1200, 1500, a//3],
        'MES 매출': [800, 1100, 1300, b//2],
        'SCADA 매출': [900, 1000, 1100, a//4]
    })

    # 라인 차트 출력
    st.line_chart(trend_data)
    
