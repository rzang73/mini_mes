
score_dic =   {           
    "Kim":[99,83,95,100,85,95 ],
    "Lee":[68,45,78,88,75,56],
    "Choi":[25,56,69,55,75,45]
}

for name, scores in  score_dic.items():
     print(name,"의 평균성적=",sum(scores)/len(scores))
     print(name,"의 최대점수=",max(scores))
     print(name,"의 최소점수=",min(scores))


text_data ="Create the highest, grandest vision possible for your life, because you become what you believe"
word_dic = {}
for w in text_data.split():		# 텍스트를 단어들로 분리하여 반복한다. 
     if w in word_dic:			# 단어가 이미 딕셔너리에 있으면
         word_dic[w]  += 1  		# 출현 횟수를 1 증가한다. 
     else:				# 처음 나온 단어이면 1로 초기화한다. 
         word_dic[w]   = 1  

for w, count in sorted(word_dic.items()):
     print(w, '의 등장회수=', count)


import collections

data ="Create the highest, grandest vision possible for your life, because you become what you believe"

str = collections.Counter(data.split())

print(type(str))
print(str)


s = input("문자열을 입력하시오: ")

s1 = s[::-1]			# 문자열을 거꾸로 만든다. 

if( s == s1 ):
        print("회문입니다.")
else:
        print("회문이 아닙니다.")

s = input("파이썬 소스 파일 이름을 입력하시오: ")

if s.endswith(".py"):
	print("올바른 파일 이름입니다")
else :
	print("올바른 파일 이름이 아닙니다.")

