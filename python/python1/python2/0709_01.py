# 2부터 20까지 2씩 건너뛰며 리스트 생성
even_list = list(range(2, 21, 2))

print(even_list)
# 출력: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

scores = [55, 80, 43, 90, 72, 61]

# 60점 이상이면 '합격', 아니면 '불합격'을 리스트에 담음
result = ['합격' if score >= 60 else '불합격' for score in scores]

print(result)

# 값이 1(불량)일 때의 위치(idx + 1)만 모아서 리스트 생성
#inspection = [0, 1, 0, 0, 1, 1, 0, 1]
#ng = [idx + 1 for idx, value in enumerate(inspection) if value == 1]
#print(ng)
# 출력: [2, 5, 6, 8]

inspection = [0, 1, 0, 0, 1, 1, 0, 1]

# 0번부터 시작하는 인덱스(idx)를 그대로 리스트에 담습니다.
ng = [idx for idx, value in enumerate(inspection) if value == 1]

print(ng)
# 출력 결과: [1, 4, 5, 7]

# 
words = ["python", "sql", "ai", "streamlit", "db", "factory"]

# 2. 리스트 표현식을 사용하여 5글자 이상인 것만 대문자로 변환
# len(w) >= 5 조건문과 w.upper() 대문자 변환 함수를 조합합니다.
result = [w.upper() for w in words if len(w) >= 8]

# 3. 결과 출력
print(result)

# 1. 원본 문자열 리스트 정의
words = ["python", "sql", "ai", "streamlit", "db", "factory"]

# 2. 리스트 표현식(Comprehension)을 활용한 필터링 및 대문자 변환
# len(w) >= 5 조건문과 w.upper() 함수를 사용합니다.
result = [w.upper() for w in words if len(w) >= 5]

# 3. 결과 출력
print(result)
# 출력: ['PYTHON', 'STREAMLIT', 'FACTORY']

words = ["python", "sql", "ai", "streamlit", "db", "factory"]
result = [w.upper() for w in words if len(w) >= 5]
print(result)

english_dict ={}			# 공백 딕셔너리를 생성한다. 

english_dict["one"]="하나"		# 딕셔너리에 단어와 의미를 추가한다. 
english_dict["two"]="둘'"		
english_dict["three"]="셋"		

word =input("단어를 입력하시오: ");
print (english_dict[word])

score_dic =   {           
    "Kim":[99,83,95],
    "Lee":[68,45,78],
    "Choi":[25,56,69]
}

for name, scores in  score_dic.items():
     print(name,"의 평균성적=",sum(scores)/len(scores))

