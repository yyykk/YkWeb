import pymysql
def Map():
    DataBase = pymysql.connect (host = "localhost", user = "root", passwd = "mysql", db = "demo", charset='utf8')
    CursorDict = DataBase.cursor(pymysql.cursors.DictCursor)
    Cursor = DataBase.cursor()
    Cursor.execute('select distinct Time from EciTimeStream;')
    Time = Cursor.fetchall()
    position = []
    counter = 0
    for t in Time:
        print(t)
        #print("select t.lng, t.lat, e.Stream / m.MStream * 100 as count from ecihourstream as e , MaxStream as m, tac as t where t.ECI = e.ECI and e.ECI = m.ECI and e.Time = '" + str(t)[2:15] + "'")
        #CursorDict.execute("select t.lng, t.lat, e.Stream as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.Time = '" + str(t)[2:21] + "'")
        #DictTemp = CursorDict.fetchall()
        #print(DictTemp) 
        #position.append(DictTemp)
        counter += 1
        if(counter - 1000 == 0):
            print(counter)
            break;
    print(position[6])
    DataBase.close()
if __name__ == '__main__':
    Map();
