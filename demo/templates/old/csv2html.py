def MyRead(FileReader):
    string = FileReader.readline();
    string = string.decode(encoding='utf-8',errors='ignore');
    return string;


if __name__ == '__main__':
    FileName = "rw";
    FileR = open(FileName + ".csv", "rb");
    FileW = open(FileName + ".html", "wb+");
    head = """
<html>
<title>
    0626
</title>
<body>
<h1> <center> <font size = 8> <b> 各小区网络质量 </b> </font> </center> </h1>
<center>
<font size = 3>
<table border='1'cellspacing=0 cellpadding=3 >
    """
    FileW.write(bytes(head, 'utf-8'))
    while(1):  
        l = MyRead(FileR);
        if (l == ""):
            break;
        l = l.replace(",", "</td><td class='onecenter'>");
        l = "<tr><td class='onecenter'>" + l[0:len(l)-1] + "</td></tr>\n";
        FileW.write(bytes(l, 'utf-8'));
    end = """
</table>
</font>
</center>
</body>
    """
    FileW.write(bytes(end, 'utf-8'));
    FileR.close();
    FileW.close();







