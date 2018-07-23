#!/usr/bin/python
#coding=utf-8 
import os
import sys
import xlwt
import codecs
import cchardet


#获取目录文件函数，输入路径，得到该目录下所有的文件,默认为脚本当前目录
def FileList(file_dir=sys.path[0]):  
    i=0   
    filelist=[]
    filesT =[]
    # print ('adfaqerasdfasdgdg')
    print (file_dir)
    for root, dirs, files in os.walk(file_dir):  
        i=i+1
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
#        print(files) #当前路径下所有非目录子文件
#每走到一层文件夹里，该文件夹的文件列出来，加上路径
        for fn in files: 
            print (fn)
            filesT.append(os.path.join(root, fn)) #把文件名加上路径
        filelist = filelist + filesT
#        print('++++',i)
    return filelist
print ('========') 
#print (FileList())    
#定义OpenFile函数，l,s,f分别为读取成LIST，单行，文件
def OpenFile(filename,filerow='l'):  
    #文件编码，默认UTF8
    FileCode = 'utf-8' 
    #两种返回结果，行LIST，字符串
    Fl = []
    Fs =''

    #编码验证函数，反回文件编码方式           
    with codecs.open(filename, "rb") as fr :
        FileContent=fr.read()
        ftype =cchardet.detect(FileContent)
#        print (ftype)
        FileCode=ftype["encoding"]
    #文件打开函数，以FileCode为打开方式
    with codecs.open(filename, "r",encoding=FileCode,errors='ignore') as fr :
        if filerow =='l' :
            Fl=fr.readlines()
        elif filerow =='f' :
            Fs=fr.read()

    #根据filerow参数决定反回结果
    if filerow =='l' :
        return Fl
    elif filerow =='f' :
        return Fs

# print(os.getcwd())
# d = os.path.dirname(__file__)
# print(d)
# f=os.path.join(d, 'HAJIY-MC-BA01-gaoxinju_180416.log')
# print(OpenFile(f,'l'))
#==================================================================
#excel整体写入函数，参数，输入列表，保存文件名
def XlsWrite(Xlsdata=[],XlsFile='test.xls'):
    wbk = xlwt.Workbook()
    sheet1 = wbk.add_sheet('sheet 1')
    XlsRow=0
    XlsCol=0
    for IpInfos in Xlsdata:   #遍历母表行
        XlsCol = 0
        for IpInfo in IpInfos:  #遍历母表列
            sheet1.write(XlsRow,XlsCol,IpInfo)  #写入EXCEL(行号，列号，内容)
#            print(IpInfo)
            XlsCol = XlsCol + 1    #列数加1
        XlsRow = XlsRow + 1        #行数加1

    wbk.save(XlsFile)


