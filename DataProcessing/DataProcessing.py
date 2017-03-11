
import time
import os

#修改NeedWord 列表能够选取不同的字段
NeedWord = ['MSISDN', 'ECI', 'APN', 'RequestTime', 'ProcedureEndTime', 'AppType', 'AppSubType',
             'AppContent', 'AppStatus', 'L4Protocal', 'AppServerIP_IPv4', 'AppServerPort',
             'ULTraffic', 'DLTraffic', 'ULTCPOoOPacket', 'DLTCPOoOPacket', 'ULTCPRetransPacket',
             'DLTCPRetransPacket', 'TCPSYNAtteDelay', 'TCPSYNComfirmDelay', 'TCPSYNSuccFirstReqDelay',
             'FirstReqToFirstResDelay', 'TCPSYNAtte', 'TCPConnStatus', 'FirstHTTPResPacketDelay',
             'LastHTTPPacketDelay', 'LastACKPacketDelay', 'HOST', 'HTTP_content_type']

#传入已经打开文件的对象,返回读取的行
def ReadFile(Reader):
    string = Reader.readline()
    string = string.decode(encoding='utf-8', errors='ignore')
    string = string.strip('\r\n')
    return string

#传入需要的字段，输出所需字段的次序
def GetOrder(NeedWord, Title):
    Title = "," + Title + ","
    OrderList = []#begin 0
    Field = ""
    Order = 0
    Second = 0
    while(1):
        First = Title.find(",", Second) + 1
        Second = Title.find(",", First + 1)
        Field = Title[First : Second]
        if (Field in NeedWord):
            OrderList.append(Order)
        Order += 1
        if(Second == len(Title) - 1):
            break;
    return OrderList

#处理某些数据逗号数量异常
def DeleteComma (String):
    CommaCount = 0
    CommaIndex = -1
    while(1):
        CommaIndex = String.find(",", CommaIndex + 1)
        CommaCount += 1;
        if(CommaCount == 52):
            String = String[0:CommaIndex] + String[CommaIndex + 1 : len(String)]#删掉多余的逗号
            break
    return String

#将读取后的数据处理之后写入最后的文件
def WriteData(String, OrderList, Writor):
    if(String.count(',') != 60):
            String = DeleteComma(String)
    String += ","
    Second = String.find(",")
    First = -1
    Order = 0
    WordCommand = ""
    WordList = []
    while(1):
        Word = String[First + 1 : Second]
        if (Order in OrderList):
            WordList.append(Word)
            Word = ""
        if(Second == len(String) - 1):
            break;
        First = String.find(",", First + 1)#因为是逗号分隔文件，所以两个逗号中间的便是我们需要的信息
        Second = String.find(",", Second + 1)
        Order += 1  
    for WordListIter in range(len(WordList)):
        WordCommand += WordList[WordListIter] + ","
    else:
        WordCommand = WordCommand[0:len(WordCommand)-1] + ",0"#因为ID是自增字段，所以为其赋值为0    
    Writor.write(bytes(WordCommand + '\n', 'utf-8'))

#从文件夹中获取待处理的文件路径列表
def GetFileList(Path):  
    FileList = []
    Files = os.listdir(Path)   
    for f in Files:
        if(os.path.isfile(Path + '/' + f)):  
            FileList.append(Path + '/' + f)  
    return FileList

#获取待处理文件名    
def GetFileName(FilePath):
    temp = 0
    while(1):
        Index = temp
        temp = FilePath.find('/', temp + 1)
        if(temp == -1):
            break
    return FilePath[Index + 1 : ]

#传入待处理文件列表    
def ReadData(Path):
    os.mkdir(r'./Ok/')#将处理后的文件全都放入这个文件夹中
    for f in Path:
        Reader = open(f, 'rb')
        Writor = open('./Ok/' + GetFileName(f), "wb+")
        Title = ReadFile(Reader)
        OrderList = GetOrder(NeedWord, Title)

        TempString = ''
        Counter = 0
        Word = ''
        StartTime = time.time()
        while(1):
               
            while(1):#去除相邻行的重复数据
                String = ReadFile(Reader)
                if(String != TempString):#如果该行数据与上一行数据不同则跳出循环
                    TempString = String#保存上一行数据
                    break
        
            if(String == ''):#读入空行则到达末尾，跳出循环
                break

            WriteData(String, OrderList, Writor)

            Counter += 1
            if (Counter % 1000000 == 0):#由于程序跑得太慢，每隔n行输出一次以便让我知道程序没有卡死
                print("right = ", Counter)
                print(time.time() - StartTime)
            if (Counter == 20000000):#每个文件处理行数，测试的时候可以设置一个较小的值
                print("pass = ", Counter)
                break

        Writor.close()    
        Reader.close()

if __name__ == '__main__':
    StartTime = time.time()
    ReadData(GetFileList('./before'))#待处理文件所在文件夹，会处理文件夹中所有文件（文件应该是原始文件）
    print(time.time() - StartTime)









    
    
