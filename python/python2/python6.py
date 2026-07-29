counter = [0]*26 
with open('/mnt/c/Temp/mobydick.txt', 'r') as infile:
    ch = infile.read(1)
    while ch != "" :
        ch = ch.upper()    
        if ch >= "A" and ch <= "Z" :
            i = ord(ch) - ord("A")
            counter[i] += 1
        ch = infile.read(1)

print(counter)
