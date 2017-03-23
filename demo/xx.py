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
        #print("select t.lng, t.lat, e.Stream as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.Time = '" + str(t)[2:6] + "'")
        CursorDict.execute("select t.lng, t.lat, e.Stream as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.Time = '" + str(t)[2:6] + "'")
        DictTemp = CursorDict.fetchall()
        #print(DictTemp) 
        position.append(DictTemp)
        counter += 1
        if(counter % 100 == 0):
            print(counter)
    print(position[6])
    DataBase.close()
if __name__ == '__main__':
    Map();
