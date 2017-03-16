import pymysql
def Map():
    DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo")
    CursorDict = DataBase.cursor(pymysql.cursors.DictCursor)
    Cursor = DataBase.cursor()
    Cursor.execute('select ECI from tac;')
    ECI = Cursor.fetchall()
    #for e in ECI:
        #print(print('select t.lng, t.lat, e.Stream from ecihourstream as e, tac as t where e.ECI = '+ str(e)[1:10] + ' and e.ECI = t.ECI;'))
    position = []
    for e in ECI:
    	CursorDict.execute('select t.lng, t.lat, e.Stream from ecihourstream as e, tac as t where e.ECI = '+ str(e)[1:10] + ' and e.ECI = t.ECI;')
    	DictTemp = CursorDict.fetchall()
    	print(DictTemp)
    	MaxStream = DictTemp['Stream'].max()
    	for i in range(len(DictTemp['Stream'])):
    		DictTemp['Stream'][i] = DictTemp['Stream'][i] / MaxStream
    	position.append(DictTemp);
    print(position)
if __name__ == '__main__':
    Map();
