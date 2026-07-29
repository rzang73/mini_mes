slist = []
for i in range(5):
   score = int(input('성적 입력 :'))
   slist.append(score)

print('성적 평균=',sum(slist) / len(slist))
print('최대점수=',max(slist))
print('최소점수=',min(slist))

cnt = 0
for score in slist:
   if score >=80:
       cnt += 1

print('80 이상 : ', cnt)
 