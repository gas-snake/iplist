#!/usr/bin/python
#coding=utf-8 
import ofile

LN= "C:\\Users\\Terisa\\Desktop\\python\\iplistall2\\HAJIZ-MC-BA01-FENGSHOULU-(2017_11_08).txt"

LOG=ofile.OpenFile(LN,'f')
LOGS=LOG.split('#\r\n')
print (type(LOG))
print (LOGS)
for l in LOGS:
    print (l)