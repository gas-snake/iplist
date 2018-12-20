#!/usr/bin/python
#coding=utf-8 

#在列表中查找某个值，反回下标，找不到返回-1
def  field_index(txt=[],field=''):
	try:
		findex=txt.index(field)
		return findex
	except Exception as  e:
		return -1

def IpSearch(LogFile=[]):
#-----------------------------------
    SeRasult=[]  #IP信息总表
    DEVinfo=[] #设备信息    
    IPpool=[]  #地址池信息   ip,mask,名称，行号
    IPinter=[] #端口信息    ip,mask,端口名称，desc，行号
    
    DHCPstatic = [] #DHCP数据 ip,端口，vlan,desc，行号
    IPstatic=[] #静态路由信息 起始IP，终止IP，端口，desc，行号
#-----------------------------------    

    fno = 0
    sysname = ''
    router_id = ''
    interface = ''
    description= ''
    vlan = ''
    interfaces=[]
#-----------------------------------
    for foline in LogFile:  #逐行读取LOG文件
        foline=foline.strip("\r\n")  #去掉回车换行
        fno+=1  #生成行号
    #    print(sum)
        if foline.startswith('sysname')== True: #判断是否为sysname开头
            lines=foline.split(' ')
            sysname = lines[1]
            DEVinfo.append(sysname)
        elif foline.startswith('router id ')== True:#判断是否为router id开头
            router_id=foline.replace('router id ','')

            DEVinfo.append(router_id)
        elif foline.startswith('vlan ') == True  :#判断是否为vlan开头
            lines=foline.split(' ')
            if lines[1] != 'batch':      #不是vlan batch 那一行
                vlan = lines[1]
        elif foline.startswith(' dhcp snooping bind-table ')== True: #判断是否DHCP开头
            lines=foline.split(' ')
            ipIn=field_index(lines,'ip-address')
            interIn=field_index(lines,'interface')
            print ('DHCP+++',lines[ipIn+1],lines[interIn+1],vlan,'',fno)
            DHCPstatic.append([lines[ipIn+1],lines[interIn+1],vlan,'',fno])
            interfaces.append(lines[interIn+1])

        elif foline.startswith('ip pool')== True: #判断是否为ip pool开头
            lines=foline.split(' ')
            interface = lines[2] 
        elif foline.startswith(' gateway')== True: #判断是否为gateway开头
            lines=foline.split(' ')     
            IPpool.append([lines[2],lines[3],interface,fno])
    #        XlsWriteRow(xlsRow,sum,sysname,interface,"",IPy.IP(lines[2]+"/"+lines[3],make_net=True).strNormal(),"",lines[3])
#            IpListMain = IpPoolInfo(IPy.IP(lines[2]+"/"+lines[3],make_net=True),lines[2],lines[3],IpListMain,sum,sysname,interface,"")
            #if  interface.startswith("guding") == True:
            #    IpListMain = IpPoolInfo(IPy.IP(lines[2]+"/"+lines[3],make_net=True),lines[2],lines[3],IpListMain,sum,sysname,interface,"")
    #            for Ip in IPy.IP(lines[2]+"/"+lines[3],make_net=True):
    #                print(Ip)
                    
                    #MakeIpList(iplistRow,sum,sysname,interface,"",Ip.strNormal(),"",lines[3])
                    #iplistRow+=1
            #else: 
            #    MakeIpList(iplistRow,sum,sysname,interface,"",IPy.IP(lines[2]+"/"+lines[3],make_net=True).strNormal(),"",lines[3])
            #    iplistRow+=1              
        elif foline.startswith('interface')== True: #判断是否为interface开头
            lines=foline.split(' ')
    #    	print(sum,lines[1],end = '')
            interface = lines[1]   #得到端口名称


        elif foline.startswith(' description')== True:   #否则判断是否为description开头
#            lines=foline.split(' ') 
            description = foline[13:]                       #更新标签内容

        elif foline.startswith(' ip address')== True:   #否则判断是否为ip address开头
            lines=foline.split(' ') 
            IPinter.append([lines[3],lines[4],interface,description,fno])
            #print(sum,interface,description,lines[3],lines[4],end = '') #得到ip值  MASK值
            # sheet1.write(xlsRow,0,sum)
            # sheet1.write(xlsRow,1,interface)
            # sheet1.write(xlsRow,2,description)
            # sheet1.write(xlsRow,3,lines[3])
            # sheet1.write(xlsRow,4,"")
            # sheet1.write(xlsRow,5,lines[4])
#            IpListMain = IpPoolInfo(IPy.IP(lines[3]+"/"+lines[4],make_net=True),lines[3],lines[4],IpListMain,sum,sysname,interface,description)
            #if (lines[3].startswith('120.194')== True or lines[3].startswith('218.206')== True ):
              
            #    for Ip in IPy.IP(lines[3]+"/"+lines[4],make_net=True):
            #        print(Ip)
            #        MakeIpList(iplistRow,sum,sysname,interface,description,Ip.strNormal(),"",lines[4])
            #        iplistRow+=1
    #        print (iplist[1])
    #        xlsRow+=1


        elif foline.startswith(' static-user')== True:   #判断是否为static-user开头
            lines=foline.split(' ')                    #拆分字符串
            print(lines[2])
            ipOp=""  #起始IP
            ipEd=""  #终止IP
            desc=''  #描述
            inter='' #端口
            gateIn=field_index(lines,'gateway')
            interIn=field_index(lines,'interface')
            if gateIn == 5 :   #是否存desc字段
                desc=lines[gateIn-3]
            #取IP
            if gateIn != -1 : #存在gateway就取IP
                ipOp=lines[gateIn-2]
                ipEd=lines[gateIn-1]

            if interIn != -1:   #是否存interface字段
                inter=lines[interIn+1]

            IPstatic.append([ipOp,ipEd,inter,desc,fno])
#            if lines[2].find('.')!=-1:    #用第二个值是否含.来判断该static-user是否有标签
            	#print(sum,lines[7],"",lines[2],lines[3])   #接是否有标签来推算 起始IP 终止IP  及端口的位置
                #sheet1.write(sum,lines[7],"",lines[2],lines[3])
                # sheet1.write(xlsRow,0,sum)
                # sheet1.write(xlsRow,1,lines[7])
                # sheet1.write(xlsRow,2,"")
                # sheet1.write(xlsRow,3,lines[2])
                # sheet1.write(xlsRow,4,lines[3])
    #            XlsWriteRow(xlsRow,sum,sysname,lines[7],"",lines[2],lines[3],"")    
 #               ipOp=lines[2]
 #               ipEd=lines[3]
 #               interface=lines[7]
 #               description=""
    #            xlsRow+=1
 #               print(".....",ipOp,ipEd)
 #           else:
            	#print(sum,lines[8],lines[2],lines[3],lines[4])
                #sheet1.write(sum,lines[8],lines[2],lines[3],lines[4])
                # sheet1.write(xlsRow,0,sum)
                # sheet1.write(xlsRow,1,lines[8])
                # sheet1.write(xlsRow,2,lines[2])
                # sheet1.write(xlsRow,3,lines[3])
                # sheet1.write(xlsRow,4,lines[4])
    #            XlsWriteRow(xlsRow,sum,sysname,lines[8],lines[2],lines[3],lines[4],"")
 #               ipOp=lines[3]
 #               ipEd=lines[4]
 #               interface=lines[8]
#                description=lines[2]
    #            xlsRow+=1
#            RowOp = 0
#            RowEd = 0
#            print("查找",ipOp,ipEd)
#            IpListMain = IpStaticInfo(ipOp,ipEd,IpListMain,sum,interface,description)
            #for R in range(0,len(iplist)-1):
            #    if iplist[R][4] == ipOp:
            #        RowOp=R
            #    if iplist[R][4] == ipEd:
            #        RowEd=R
            #        break
            #print("已找到行",RowOp,RowEd)
            #for R in range(RowOp,RowEd+1):
            #    iplist[R][0] = sum
            #    iplist[R][2] = interface
            #    iplist[R][3] = description
            #    print("RowOp=",RowOp,"*****","RowEd=",RowEd,"description=",description)

            
        elif foline.startswith('#')== True:
            interface =''
            description = ""       #更新端口时清空标签值

        #有端口有描述的情况下，对比DHCPstatic，补上描述
        if interface != '' and description != '':
            for dhcp in DHCPstatic:
                if dhcp[1] == interface:
                    dhcp[3]=description
    SeRasult.append(DEVinfo)
    SeRasult.append(IPpool)
    SeRasult.append(IPinter)
    SeRasult.append(DHCPstatic)
    SeRasult.append(IPstatic)
    # print('DEVinfo',DEVinfo)
    # print('IPpool',IPpool)
    # print('IPinter',IPinter)

    return SeRasult

def PortSearch(LogFile=[]):
#-----------变量定义------------------------
    SeRasult=[]  #信息总表
    temp=[]       #暂存一行信息
    sn= 0         #行号
    sysname = "" #设备名称  
    interface = ""  #变量 端口
    intertype = ""  #变量 端口类型 主端口，sub端口
    description = ""#变量 标签
    interip = ""    #变量  ip
    intermask = ""  #变量 mask
    eth = "" #物理端口对应的eth-trunk
    status = ""    #物理端口状态
    portOn = "0"
    # SubInterW = "N"  #是否保存子端口
    #Mode值为M或A,分别为主端口和全端口


# fo = open(LogFileName+".log", "rb")
# folines = fo.readlines() 
    for foline in LogFile:
        # foline = foline.decode("utf_8").strip("\r\n")
        foline = foline.rstrip().strip("\r\n")
        sn+=1 
        if foline.startswith('sysname')== True: #判断是否为sysname开头
            lines=foline.split(' ')
            sysname = lines[1].strip("\r\n")
        elif foline.startswith('interface')== True: #判断是否为interface开头
            # descOn = ""
            portOn = "1"   #是interface开头则打开写入开关
            lines=foline.split(' ')
            if lines[1].find(".") != -1:      #端口名称中有.即为子端口,tpye里写入sub
                intertype = "sub"
#    	print(sum,lines[1],end = '')
                # SubInterW = 'Y'           #是主端口，可以写入      
            interface = lines[1].strip("\r\n")   #得到端口名称
            # print(interface)
                # descOn = "1"                        #如果端口中没有. 可以采desc，否则不采  
                # description = ""  
                             #为防采错，在此处把DESC清空
        elif foline.startswith(' description')== True:   #否则判断是否为description开头
            lines=foline.split(' ') 
            description = foline.replace(' description','')
            # if descOn =="1":
            #     description = foline.replace(' description','')
            #     print(description)
        elif foline.startswith(' ip address')== True:   #否则判断是否为ip address开头
            lines=foline.split(' ') 
            interip =lines[3]
            intermask =  lines[4]
        elif foline.strip("\r\n").startswith(' eth-trunk')== True:   #否则判断是否为 eth-trunk开头
            eth = foline.strip("\r\n")
            # print(eth)
        elif foline.strip("\r\n").startswith(' shutdown')== True:#否则判断是否为 shut
            status = foline.strip("\r\n")
            # print(status)
        elif foline.strip("\r\n").startswith('#')== True:   #否则判断是否为 #结尾
    #    lines=foline.split(' ') 
            # print(foline.strip("\r\n"))
            # print(sn,sysname,interface,intertype,description,intermask,interip,eth,status)
            # if SubInterW == 'Y' :       #结尾的时候，如果是主端口则写入                  
            # XlsWriteRow(sn,sysname,interface,description,eth,ports)
            #拼成一行信息
            temp.append(sn)
            temp.append(sysname)
            temp.append(interface)
            temp.append(intertype)
            temp.append(description)
            temp.append(interip)
            temp.append(intermask)
            temp.append(eth)
            temp.append(status) 
            if portOn == '1' :
                #把该行信息写入信息表
                SeRasult.append(temp)
            #写入完成信息清零------------------------
            interface = ""
            intertype = ""
            description = ""
            interip = ""
            intermask = "" 
            eth = ""                     
            status = ""
            temp = []
            portOn = '0'
            
        # XlsWriteRow(sum,sysname,interface,description,"")
    print("*************************")

    #elif foline.strip("\r\n").startswith(' eth-trunk')== True:   #否则判断是否为 eth-trunk开头
    #    XlsWriteRow(sum,sysname,interface,description,foline

    return SeRasult