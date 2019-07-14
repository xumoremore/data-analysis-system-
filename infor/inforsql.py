import pymysql

class InforSql(object):
    def __init__(self, ):
        self._conn = pymysql.connect(host="localhost",
                               user="root",
                               password="xuzhenchu",
                               database="senyan")
        self._cursor = self._conn.cursor()



    def readdata( self, sitenum, dataname ):
        self._sitenum = "point" + sitenum
        self._dataname = dataname
        select_data = "select Time,{} from {} where to_days(Date) = to_days(now())"
        print(select_data.format( self._dataname, self._sitenum ))
        try:
            self._cursor.execute( select_data.format( self._dataname, self._sitenum ) )
            result = self._cursor.fetchall()
            self._conn.commit()
            return result
        except:
            print("获取数据不成功")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()

    def readall( self, sitenum ):
        self._sitenum = "point" + sitenum
        select_data = "select Time,temp, air_humi, soil_humi, daily_rain from {} where to_days(Date) = to_days(now())"
        print(select_data.format( self._sitenum ))
        try:
            self._cursor.execute( select_data.format( self._sitenum ) )
            result = self._cursor.fetchall()
            self._conn.commit()
            print("获取数据成功")
            print(result)
            return result
        except:
            print("获取数据不成功")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()

    def readpredict( self, sitenum ):
        self._sitenum = "point" + sitenum
        select_data = "select temp, air_humi, soil_humi, daily_rain from {} where to_days(Date) = to_days(now())"
        print(select_data.format( self._sitenum ))
        try:
            self._cursor.execute( select_data.format( self._sitenum ) )
            result = self._cursor.fetchall()
            self._conn.commit()
            print("获取数据成功")
            print(result)
            return result
        except:
            print("获取数据不成功")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()