import os
f = open("test.txt","r")
inp = []
for line in f:
    inp.extend(line.split())
inps = "".join(inp)
f.close()
#print "python nkcohcoh.py 3 3 "+inps+" 5"
os.system("python nkcohcoh.py 4 3 "+inps+" 15")
