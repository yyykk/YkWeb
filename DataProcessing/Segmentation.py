import os

def ReadFile():
    text = FileReader.readline()
    text = text.decode(encoding='utf-8',errors='ignore')
    return text

def Segmentation(FileName):
    counter = 1;
    while(1):
        FileWriter = open('./' + FileName + '/' + FileName + '_' + str(counter) + '.txt', "wb+")
        num = 0;
        while(1):
            text = ReadFile();
            if(text == ''):
                return
            if (num == 1000000):
                break
            FileWriter.write(bytes(text, 'utf-8'))
            num += 1;
        print(counter)
        counter += 1;
        FileWriter.close();

if __name__ == '__main__':

    FileName = 'http_0627_gaoxiao.txt'#需要输入处理文件名
    FileReader = open(FileName, 'rb')
    Index = FileName.find('.')

    os.mkdir(FileName[:Index])
    Segmentation(FileName[:Index])
    FileReader.close();


