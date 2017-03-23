import pymysql
import os
import time

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

def LoadData(Path):
    #需将其改为自己的数据库名字还有密码
    DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo")
    cursor = DataBase.cursor()
    for p in Path:
        #print("load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/" + p[1:] + "' into table `motorwayhttp` fields terminated by ',';");
        cursor.execute("load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/" + p[1:] + "' into table `motorwayhttp` fields terminated by ',';")
        DataBase.commit();
    DataBase.close()
        

if __name__ == '__main__':
    StartTime = time.time()
    Path = GetFileList('./MS_S1_U_Http_0711_gaosu')#待处理文件所在文件夹，会处理文件夹中所有文件（文件应该是原始文件）
    #print(Path)
    LoadData(Path)
    print(time.time() - StartTime)
