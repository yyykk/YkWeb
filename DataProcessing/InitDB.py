import pymysql

#需将其改为自己的数据库名字还有密码
DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo")
cursor = DataBase.cursor()

#NeedWord是数据库中建表的字段
NeedWord = ['MSISDN', 'ECI', 'APN', 'RequestTime', 'ProcedureEndTime', 'AppType', 'AppSubType',
             'AppContent', 'AppStatus', 'L4Protocal', 'AppServerIP_IPv4', 'AppServerPort',
             'ULTraffic', 'DLTraffic', 'ULTCPOoOPacket', 'DLTCPOoOPacket', 'ULTCPRetransPacket',
             'DLTCPRetransPacket', 'TCPSYNAtteDelay', 'TCPSYNComfirmDelay', 'TCPSYNSuccFirstReqDelay',
             'FirstReqToFirstResDelay', 'TCPSYNAtte', 'TCPConnStatus', 'FirstHTTPResPacketDelay',
             'LastHTTPPacketDelay', 'LastACKPacketDelay', 'HOST', 'HTTP_content_type', 'ID']

print(len(NeedWord))
KeyWord = ["ID"]

cursor.execute("drop table HttpTest")
LongTitle = ["HOST","HTTP_content_type"]#有些字段太长

for KeyIter in range (len(KeyWord)):
    if(KeyIter == 0):
        KeyWordString = "(" + KeyWord[KeyIter]
    else:
        KeyWordString = KeyWordString + ", " + KeyWord[KeyIter]
else:
    KeyWordString += ");"
       
for TableIter in range (len(NeedWord)):
    if (TableIter == 0):
        cursor.execute("create table HttpTest (" + NeedWord[TableIter] + " char(30));")
    else:
        cursor.execute("alter table HttpTest add " + NeedWord[TableIter] + " char(30);")
    if (NeedWord[TableIter] in LongTitle):
        print("alter table HttpTest modify " + NeedWord[TableIter] + " char(200) not null;")
        cursor.execute("alter table HttpTest modify " + NeedWord[TableIter] + " char(200) not null;")
    if (NeedWord[TableIter] in NeedWord):
        cursor.execute("alter table HttpTest modify " + NeedWord[TableIter] + " char(30) not null;")

cursor.execute("alter table HttpTest add constraint pk_orderinfo PRIMARY KEY" + KeyWordString)
cursor.execute("alter table HttpTest modify ID integer auto_increment")
cursor.execute("alter table HttpTest modify HOST char(200) null;")
cursor.execute("alter table HttpTest modify HTTP_content_type char(200) null;")

DataBase.close()
