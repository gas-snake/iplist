#!/usr/bin/python
#coding=utf-8 
import ofile

LN= "C:\\Users\\Terisa\\Desktop\\python\\iplistall2\\HAJIZ-MC-BA01-FENGSHOULU-(2017_11_08).txt"
LN2="C:\\Python\\TEST\\HAJIY-MC-BA01-gaoxinju_170831.log"
# LOG=ofile.OpenFile(LN,'f')
# LOGS=LOG.split('#\r\n')
# print (type(LOG))
# print (LOGS)
# for l in LOGS:
#     print (l)

LOG=ofile.OpenFile(LN2,'l')

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
        
        t=[]
    else :
        t.append(l)
    LOGS.append(t)
    
print (LOGS)
print ("88888888")
print (LOGS[15])
print (LOGS[35])
print (LOGS[75])
print (LOGS[105])