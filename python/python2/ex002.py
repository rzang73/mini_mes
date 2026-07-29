import csv

with open('/mnt/c/Temp/weather.csv', 'r')	as infile:
    data = csv.reader(infile)
    header = next(data)
    temp = 1000
    for row in data:
        if temp > float(row[3]):
            temp = float(row[3])
print('가장 추웠던 날은', temp, '입니다')
    