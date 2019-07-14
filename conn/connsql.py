import pymysql
import datetime
class ConnSql(object):
    def __init__(self, ):
        self._conn = pymysql.connect(host="localhost",
                               user="root",
                               password="xuzhenchu",
                               database="senyan")
        self._cursor = self._conn.cursor()

    def exist_site(self):
        create_siteinfor = "create table if NOT  EXISTS siteinfor(siteid varchar(20),N float(10), W float(10), phone varchar(20),  primary key(siteid))"
        select_site = "select siteid from siteinfor"
        exist_sitelist = []
        try:
            self._cursor.execute( select_site )
            exist_sitenum = self._cursor.fetchall()
            '''
            将读取到的数据库数据如：((1,), (2,), (3,), (5,), (6,), (7,))
            转换为列表[1, 2, 3, 5, 6, 7]
            '''
            for item in exist_sitenum:
                for i in item:
                    exist_sitelist.append(i)
            print(exist_sitelist)
            self._conn.commit()
        except:
            self._cursor.execute(create_siteinfor)
            print("新建siteinfor数据表成功")
            self._conn.commit()
    # finally:
        return exist_sitelist
        self._cursor.close()
        self._conn.close()

    def writedata(self, comdata ):
        receivedata = comdata
        sitenum = receivedata.pop(0)
        sitenum = "point" + sitenum
        receivedata = tuple( receivedata )
        insert_data = "insert into " + sitenum + " values(%s,%s,%s,%s,%s,%s)"
        #insert_data = "insert into point1 values(%s,%s,%s,%s,%s,%s)"
        print(insert_data)
        print("connsql接收到的数据为：")
        print(receivedata)
        try:
            self._cursor.execute( insert_data, receivedata )
            self._conn.commit()
            print("串口接收数据写入成功")
        except:
            print("串口数据写入不成功")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()

    def readdata( self, sitenum ):
        self.sitenum = sitenum
        select_infor = "select * from siteinfor where siteid=%s"
        try:
            self._cursor.execute( select_infor%self.sitenum )
            result = self._cursor.fetchall()   #获取到的结果为：((1, 1.0, 11.0, '1'),)
            self._conn.commit()
            print(result[0])
            return result[0]    #返回一个元祖，并且该元祖为一个单位
        except:
            print("检索不到siteid")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()

    def read_avgdata(self):
        select_site = "select siteid from siteinfor"
        exist_sitelist = []
        self._cursor.execute(select_site)
        exist_sitenum = self._cursor.fetchall()
        '''
        将读取到的数据库数据如：((1,), (2,), (3,), (5,), (6,), (7,))
        转换为列表[1, 2, 3, 5, 6, 7]
        '''
        for item in exist_sitenum:
            for i in item:
                exist_sitelist.append(i)

        print(exist_sitelist)
        try:
            for siteid in exist_sitelist:
                sitenum = "point" + siteid
                select_avgdata = "select temp, air_humi, soil_humi, daily_rain from {} where to_days(Date) = to_days(now())"
                print( select_avgdata )
                self._cursor.execute( select_avgdata.format( sitenum ) )
                todaydata = self._cursor.fetchall()
                print(todaydata)

                temp =0
                air_humi = 0
                soil_humi = 0
                daily_rain = 0
                avgdata = []
                data_cla = [temp, air_humi, soil_humi, daily_rain]

                for y in range( len(data_cla) ):
                    print(len(todaydata))
                    for i in range( len(todaydata) ):
                        print(todaydata[i][y])
                        data_cla[y] += todaydata[i][y]
                    print("int(data_cla[y]/len(todaydata)):%s"%int(data_cla[y]/len(todaydata)))
                    avgdata.append( int(data_cla[y]/len(todaydata)) )
                print("站点{}的平均数据为：{}".format( siteid, avgdata ))

                datestr = datetime.date.today().strftime("%Y-%m-%d")
                avgdata.insert(0, datestr)
                print("avgdata:%s"%avgdata)
                self.write_avgdata( siteid=siteid, writedata=avgdata )
            print("avgdata:%s"%avgdata)
            self._conn.commit()                 #如果不提交事务的话数据无法写入数据库
        except:
            print("检索不到siteid")
            self._conn.rollback()
        finally:
            self._cursor.close()
            self._conn.close()

    def write_avgdata(self, siteid, writedata):
        print("siteid:%s"%siteid)
        self.writedata = writedata
        self.tablename = "point%s_avg24"%siteid
        print("self._avgdata:%s"%self.writedata)
        insert_data = "insert into " + self.tablename + " values(%s,%s,%s,%s,%s)"
        # insert_data = "insert into point1 values(%s,%s,%s,%s,%s,%s)"
        print(insert_data)
        self._cursor.execute(insert_data, self.writedata)
