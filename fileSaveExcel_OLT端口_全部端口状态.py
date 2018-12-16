#!/usr/bin/python
#coding=utf-8 
#导出全部端口的标签及状态，含ETH 物理端口，不含子接口
import os
import xlwt
import re
import ofile
wbk = xlwt.Workbook()
sheet1 = wbk.add_sheet('sheet 1')
sum=0           #变量 行号
xlsRow = 1
xlsCol = 0
sysname = "" #设备名称
interface = ""  #变量 端口
description = ""#变量 标签
InterFaceTemp = ""
eth = "" #变量 Eth
ports = "" #变量 端口状态
descOn = ""     #状态，是否提取DESC
portOn = ""    #判断是否进行端口段
LogFileName = "PortInfo"  #文件名

Fpath=os.path.dirname(os.path.realpath(__file__))
Lpath=os.path.join(Fpath,'LogFile')
print (Fpath)
print (Lpath)

def XlsWriteRow(TxtRowNum,SysName,InterFace,DescTxt,EthName,PortStatus):
    global InterFaceTemp
    global xlsRow
    if (InterFaceTemp != InterFace):                        #当前端口是否等于输入端口，不等则写入。防止重复端口     
        sheet1.write(xlsRow,0,TxtRowNum)
        sheet1.write(xlsRow,1,SysName)
        sheet1.write(xlsRow,2,InterFace)
        sheet1.write(xlsRow,3,DescTxt)
        sheet1.write(xlsRow,4,EthName)
        sheet1.write(xlsRow,5,PortStatus)
        xlsRow+=1
        InterFaceTemp = InterFace                           #把写入的端口放入TEMP，用来对比
    else:
        print ("-----------------端口错误----------")
    return
#def XlsWriteRow(xlsRow,TxtRowNum,SysName,InterFace,DescTxt,EthName):
#                        #当前端口是否等于输入端口，不等则写入。防止重复端口     
#    sheet1.write(xlsRow,0,TxtRowNum)
#    sheet1.write(xlsRow,1,SysName)
#    sheet1.write(xlsRow,2,InterFace)
#    sheet1.write(xlsRow,3,DescTxt)
#    sheet1.write(xlsRow,4,EthName)
#    InterFaceTemp = InterFace                           #把写入的端口放入TEMP，用来对比
#    return
sheet1.write(0,0,"脚本行号")
sheet1.write(0,1,"设备名称")
sheet1.write(0,2,"端口名称")
sheet1.write(0,3,"端口描述")
sheet1.write(0,4,"Eth-Trunk")
sheet1.write(0,5,"端口状态")

print ('=====================循环取出文件===========================')
#------------------------------------------------------- 
LogFileList=[]                          #LOG文件列表
print ('Lpath',Lpath)
FileList = ofile.FileList(Lpath)  #取指定文件夹里的所有文件
print('--------')
print ('FileList',FileList)
for fl in FileList:                       #过滤出LOG文件组成新列表
    print (fl)
    if os.path.splitext(fl)[1] == '.log' or os.path.splitext(fl)[1] == '.txt':
        LogFileList.append(fl)
print (LogFileList)
#-------------------------------------------------------  
#从LOG文件列表中巡环取出文件
for LogFile in LogFileList:
    folines = ofile.OpenFile(LogFile,'l')   #读取脚本到folines#
# fo = open(LogFileName+".log", "rb")
# folines = fo.readlines() 
    for foline in folines:
        # foline = foline.decode("utf_8").strip("\r\n")
        foline = foline.strip("\r\n")
#    foline = foline.strip("\r\n")
        sum+=1 
        if foline.startswith('sysname')== True: #判断是否为sysname开头
            lines=foline.split(' ')
            sysname = lines[1].strip("\r\n")
        elif foline.startswith('interface')== True: #判断是否为interface开头
            descOn = ""
#        portOn = "1"
            lines=foline.split(' ')
            if lines[1].find(".") == -1:      #端口名称中没有.即为主端口，可以采名称和标签
            
#    	print(sum,lines[1],end = '')

                interface = lines[1].strip("\r\n")   #得到端口名称
                print(interface)
                descOn = "1"                        #如果端口中没有. 可以采desc，否则不采  
                description = ""  
                             #为防采错，在此处把DESC清空
        elif foline.startswith(' description')== True:   #否则判断是否为description开头
            lines=foline.split(' ') 
            if descOn =="1":
                description = foline.replace(' description','')
                print(description)
        elif foline.strip("\r\n").startswith(' eth-trunk')== True:   #否则判断是否为 eth-trunk开头
            eth = foline.strip("\r\n")
            print(eth)
        elif foline.strip("\r\n").startswith(' shutdown')== True:#否则判断是否为 shut
            ports = foline.strip("\r\n")
            print(ports)
        elif foline.strip("\r\n").startswith('#')== True:   #否则判断是否为 #结尾
    #    lines=foline.split(' ') 
            print(foline.strip("\r\n"))
            print(sum,sysname,interface,description,eth,ports)
            XlsWriteRow(sum,sysname,interface,description,eth,ports)
            eth = ""
            ports = ""
        # XlsWriteRow(sum,sysname,interface,description,"")
print("*************************")

    #elif foline.strip("\r\n").startswith(' eth-trunk')== True:   #否则判断是否为 eth-trunk开头
    #    XlsWriteRow(sum,sysname,interface,description,foline)
print(Fpath)

# wbk.save(os.path.join(Fpath,LogFileName+'端口.xls')) 