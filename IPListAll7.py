#!/usr/bin/python
#coding=utf-8 
import IPy
import os
import sys
import ofile
import LOGsearch_HuaWei
#=====================定义区===========================
#SubNetList = [
#'218.206.220.0/22', 
#'120.194.224.0/21', 
#'112.53.99.0/24'];              #需要核查的子网列表
SubNetList = []
#SubNetList = [
#'218.206.220.0/29', 
#'120.194.224.0/30', 
#'112.53.99.0/28'];              #需要核查的子网列表

# LogFileList = []
IpListMain = []                  #IP地址主列表

#Fpath=os.path.dirname(__file__)  #当前路径  
Fpath=os.path.dirname(os.path.realpath(__file__))
Lpath=os.path.join(Fpath,'LogFile')
#=====================



# Ip = []
# iplist=[]
# ipinfo=[]
# iplistRow = 0
# iplistCol = 0
# IpInfoSheet=[]

XlsName = 'IP核查.xls'
print ('======================输入列表==========================')
# print (SubNetList)
# print (LogFileList)

#******************************
"""列表字段
IP
所在子网
掩码
网关地址
广播地址
IP类型
所在设备
行号
端口
描述"""


#=====================函数区===========================

def SubNet_disband(SubNetTxt):          #函数，把子网展开
    IpList =[]
    IpInfo = []
    i = 0
    SubNet=IPy.IP(SubNetTxt,make_net=True) #把子网字符串转成标准IPy类型
#    print(SubNet)
#    print("ipinfo:",IpInfo)
#    print("IpList:",IpList)
    #for IP in SubNet:                      #输出每一个IP
    #    print(IP,SubNet,SubNet.netmask(),SubNet.broadcast())
    for IP in SubNet:
        #print(IP.strNormal(0))
        IpInfo.append(IP.strNormal(0))         #单个IP
        IpInfo.append('')         #所在子网
        IpInfo.append('')            #掩码
        IpInfo.append('')                      #网关地址
        IpInfo.append('')          #广播地址
        IpInfo.append('')                      #IP类型
        IpInfo.append('')                      #所在设备
        IpInfo.append('')                      #所在行号
        IpInfo.append('')                      #端口
        IpInfo.append('')                      #描述
        #print(i,"周")
        #i=i+1
        #print("ipinfo:",IpInfo)
        IpList.append(IpInfo)
        #print("IpList:",IpList)
        IpInfo=[]
    #print(IpList)
    return  IpList

#def SubNet_disband(SubNetTxt):          #函数，把子网展开
#    SubNet=IPy.IP(SubNetTxt,make_net=True) #把子网字符串转成标准IPy类型
#    print(SubNet)
#    for IP in SubNet:                      #输出每一个IP
#        print(IP)

def IpPoolInfo(IpPool,Gate,Mask,IpList,fn,sysname,interface,DescTxt):          #把IPPOOL刷入主表
    IpNet = IpPool.net().strNormal()
    Ipbroad = IpPool.broadcast().strNormal()
    IpTotal = len(IpPool)
    WtYes = 'N'                                     #写入开关
    for R in range(0,len(IpList)):                      #遍历主表
        if IpList[R][0] == IpNet:
            WtYes = 'Y'                             #如果找到该段IP的开头，则打开写入开关
        if WtYes == 'Y':
            if IpList[R][0] == IpNet:
                IpType = "网络号"
            elif IpList[R][0] == Gate:
                IpType = "网关"
            elif IpList[R][0] == Ipbroad:
                IpType = "广播地址"
            IpList[R][1] = IpPool.strNormal(1)           #在该IP行写入子网信息
            IpList[R][2] = Mask                    #在该 IP行写入掩码
            IpList[R][3] = Gate        #在该IP行写入网关
            IpList[R][4] = Ipbroad       #在该IP行写入广播地址
            IpList[R][5] = IpType      #在该IP行写入IP类型
            IpList[R][6] = sysname       #在该IP行写入所在设备
            IpList[R][7] = fn       #在该IP行写入行号
            IpList[R][8] = interface       #在该IP行写入端口
            if IpType != '':
                IpList[R][9] = sysname       #如果IPTYPE为网关等，在该IP行写入本设备描述
            else:
                IpList[R][9] = DescTxt       #否则在该IP行写入对应描述
            IpType = ""
        if IpList[R][0] == Ipbroad:          #如果找到该段IP的结尾，则关闭写入开关
            WtYes = 'N'
    return  IpList

def IpStaticInfo(Ip1,Ip2,IpList,fn,interface,DescTxt):          #把Static刷入主表
    IpNet = Ip1
    Ipbroad = Ip2
    WtYes = 'N'                                     #写入开关
    for R in range(0,len(IpList)-1):                      #遍历主表
        if IpList[R][0] == IpNet:
            WtYes = 'Y'                             #如果找到该段IP的开头，则打开写入开关
        if WtYes == 'Y':
            IpList[R][7] = fn       #在该IP行写入行号
            IpList[R][8] = interface       #在该IP行写入端口
            IpList[R][9] = DescTxt       #在该IP行写入描述
        if IpList[R][0] == Ipbroad:          #如果找到该段IP的结尾，则关闭写入开关
            WtYes = 'N'
    return  IpList


#=====================业务区===========================
print ('=====================循环取出SubNet===========================')
#-------------------------------------------------------------------------------
print (Fpath)
iniName=os.path.join(Fpath, 'IP_SubNet.ini')  #拼出绝对路径
folines = ofile.OpenFile(iniName,'l') #读取全部内容  
for foline in folines:
    foline =foline.strip("\r\n")       #去掉回车换行
#    print (foline)
    if foline != '':
        SubNetList.append(foline)         #把新一行加入列表
#print(SubNetList)        
# for SubNet in SubNetList:
#     print (IPy.IP(SubNet,make_net=True))

print ('=====================把每一个SubNet打开===========================')
for SubNetTxt in SubNetList:            #把子网列表中的每一个子网送到SubNet_disband展开,并将返回的列表拼成一个母表
    IpListMain.extend(SubNet_disband(SubNetTxt))
print('IPListMain:',IpListMain)

print ('=====================循环取出文件===========================')
#------------------------------------------------------- 
LogFileList=[]                          #LOG文件列表
# print ('ssdfsasdfadfasdfasdf')
# print ('Fpath',Fpath)
print ('Lpath',Lpath)
# print ('__file__',__file__)
# print ('os.path.realpath(__file__)',os.path.realpath(__file__))
# print ('os.path.realpath(__file__)2',os.path.dirname(os.path.realpath(__file__)))
# print ('using sys.executable:', repr(os.path.dirname(os.path.realpath(sys.executable))))
# print ('using sys.argv[0]:',    repr(os.path.dirname(os.path.realpath(sys.argv[0]   ))))
# print ('sys.argv[0]',sys.argv[0])
# print ('sys.path[0]',sys.path[0])

FileList = ofile.FileList(Lpath)         #取指定文件夹里的所有文件
# print (FileList)
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
    # print (LogFile)
    folines = ofile.OpenFile(LogFile,'l')   #读取脚本到folines#
    Res=LOGsearch_HuaWei.IpSearch(folines) #把脚本丢给LOGsearch取出IP信息
    # print (Res)
    # print("1111111111111qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq11111111111")
    # print(Res[1])

    #把IPpool刷入主表
    # print("res0",Res[0])
    # print("res1",Res[1])
    # print("res2",Res[2])
    for pool in Res[1]:
        # print("ssssssssssssssssssss",pool )
        IpPoolInfo(IPy.IP(pool[0]+"/"+pool[1],make_net=True),pool[0],pool[1],IpListMain,pool[3],Res[0][0],pool[2],'')
    # print("1111111111111qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq11111111111")
    # print (IpListMain)    
    #把IPinter刷入主表 IpPoolInfo(IpPool,Gate,Mask,IpList,fn,sysname,interface,DescTxt): 
    #sysname来自Res[0][0]，如脚本配置问题这里没有写router id sysname侧会无法引用导致错误
    for inter in Res[2]:
        # print ("inter==",inter)
        IpPoolInfo(IPy.IP(inter[0]+"/"+inter[1],make_net=True),inter[0],inter[1],IpListMain,inter[4],Res[0][0],inter[2],inter[3])
    #把static-user刷入主表IpStaticInfo(Ip1,Ip2,IpList,fn,interface,DescTxt)
    print ('++dhcp++',Res[3])
    for dhcp in Res[3]:
        IpStaticInfo(dhcp[0],dhcp[0],IpListMain,dhcp[4],dhcp[1],dhcp[3])
        #把static-user刷入主表IpStaticInfo(Ip1,Ip2,IpList,fn,interface,DescTxt)
    print ('++static++',Res[4])
    for static in Res[4]:
        IpStaticInfo(static[0],static[1],IpListMain,static[4],static[2],static[3])    


    
# for Ipinfo in IpListMain:
#     print(Ipinfo)

#print(len(IpListMain))
#===================写入EXCEL=========================
#编写XLS表格表头
XlsTitle=["IP","所在子网","掩码","网关地址","广播地址","IP类型","所在设备","行号","端口","描述"]
#定义需写入的整合表格
XlsData=[]
#在整合表写入表头
XlsData.append(XlsTitle)
#拼合主表
# print("111111111111111111111111")
# print(IpListMain)
XlsData=XlsData+IpListMain
#给文件名加绝对路径
XlsName=os.path.join(Fpath, XlsName) 
#写入文件
ofile.XlsWrite(XlsData,XlsName)

