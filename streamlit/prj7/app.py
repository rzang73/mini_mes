
import streamlit as st

name = st.text_input(
    '이름',
    placeholder='이름을 입력하세요')

age = st.number_input('나이',
                      min_value =20,
                      max_value =60)

birthday = st.date_input('입사일')

st.write(name)
st.write(age)
st.write(birthday)

###### 체크 박스

agree = st.checkbox("동의합니다.")
if agree:
    st.write("동의 완료")
else:
    st.write("동의하지 않음")

###### 라디오 버튼

gender = st.radio(
    "성별",
    ["남성", "여성"]
)
st.write(gender)

##########################
# SelectBox
###########################


dept = st.selectbox(
    '부서',
    [
        '품질보증팀',
        '생산팀',
        '설비팀',
        'AI개발팀'

    ]
    )

st.write(dept)



##########################
# Multi SelectBox
###########################



skills = st.multiselect(
    "보유 기술",
    [
        "Python",
        "C++",
        "SQL",
        "PLC",
        "ROS"
    ]
)

st.write(skills)


#슬라이더

score = st.slider(
    "평가 점수",
    0,
    100
)

experience = st.slider(
    "경력(년)",
    0,
    30,
    5
)