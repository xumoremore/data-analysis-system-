import pymysql

class GraphSql(object):
    def __init__(self, ):
        self._conn = pymysql.connect(host="localhost",
                               user="root",
                               password="xuzhenchu",
                               database="senyan")
        self._cursor = self._conn.cursor()

    '''
        def exist_site(self):
            select_site = "select siteid from siteinfor"
            exist_sitelist = []
            try :
                self._cursor.execute( select_site )
                exist_sitenum = self._cursor.fetchall()

                for item in exist_sitenum:
                    for i in item:
                        exist_sitelist.append(i)
                print(exist_sitelist)
                self._conn.commit()
            except:
                self._conn.rollbak()
            finally:
                return exist_sitelist
                self._cursor.close()
                self._conn.close()
    '''
    def readdata( self, sitenum, dataname ):
        self._sitenum = "point" + sitenum
        self._dataname = dataname
        select_data = "select time,{} from {} where to_days(Date) = to_days(now())"
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
        select_data = "select time,temp, air_humi, soil_humi, daily_rain from {} where to_days(Date) = to_days(now())"
        print(select_data.format( self._sitenum ))
        try:
            self._cursor.execute( select_data.format( self._sitenum ) )
            result = self._cursor.fetchall()
            self._conn.commit()
            return result
        except:
            print("获取数据不成功")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()