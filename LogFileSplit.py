#!/usr/bin/python
#coding=utf-8 
import ofile

LN= "C:\\Users\\Terisa\\Desktop\\python\\iplistall2\\HAJIZ-MC-BA01-FENGSHOULU-(2017_11_08).txt"

# LOG=ofile.OpenFile(LN,'f')
# LOGS=LOG.split('#\r\n')
# print (type(LOG))
# print (LOGS)
# for l in LOGS:
#     print (l)

LOG=ofile.OpenFile(LN,'l')

print (type(LOG))
print (LOG)
print ('=======')
LOGS = []
t = []
for l in LOG:
    l=l.strip("\r\n")
    # print (l)
    
    # print (t)
    if l=="#":
        LOGS.append(t)
        t=[]
    t.append(l)
print (LOGS)
print (LOGS[15])
print (LOGS[35])
print (LOGS[75])
print (LOGS[105])