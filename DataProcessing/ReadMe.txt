一、DataProcessing.py

1.该处理程序有50%的压缩率，即3G的文件处理后约1.5G。
2.将需要处理数据放置于before文件夹中（在程序中可以修改文件夹名字），程序会自动地将before文件夹中的所有文件处理后以原名保存至Ok文件夹中。
3.处理程序运行速度较慢，约9秒10W行。
4.该处理程序只能处理http的原始数据。


二、InitDB.py

1.可将DataProcessing.py处理过的数据导入该脚本初始化后的数据库，只要两个程序取的字段相同。
2.导入数据时有可能会因为一次导入数据过多导致数据库卡死，所以最好将处理后的数据使用Segmentation.py分段后导入。
3.导入数据时可使用SQL语句
'load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/http10/http2.txt' 
into table `HttpTest`
fields terminated by ',';'


三、Segmentation.py

1.将文本分割为每100W行一个文件。
2.需要在代码中修改处理文件名。
3.该程序一次只能修改一个文件，且需与待处理文件在同一个文件夹中。
