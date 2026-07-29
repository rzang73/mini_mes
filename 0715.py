try:
    fname = input('파일이름입력:')
    infile = open(fname, 'r')
except IOError as e:
    print(e)  ## 연습용...