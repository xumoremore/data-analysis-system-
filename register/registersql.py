import pymysql
from tkinter import messagebox
class RegisterSql(object):
    def __init__(self, message):
        self._message = message
        self._conn = pymysql.connect(host="localhost",
                               user="root",
                               password="xuzhenchu",
                               database="senyan")
        self._cursor = self._conn.cursor()
        self._tablename = "point%s"%self._message[0]
        self._tableavg24name = "point%s_avg24"%self._message[0]
    def createtable(self):
        print(self._tableavg24name )
        create_site = "create table %s ( Date date, Time time, temp int(10), air_humi int(10), soil_humi int(10), daily_rain int(10), constraint DateTime primary key(Date, Time))"
        create_siteavg24 = "create table %s ( Date date, temp int(10), air_humi int(10), soil_humi int(10), daily_rain int(10),  primary key(Date))"
        insert_site = "insert into siteinfor( siteid, N, W, phone ) values ( %s, %s, %s, %s )"
        try:
            self._cursor.execute( create_site%self._tablename )
            self._cursor.execute( create_siteavg24%self._tableavg24name)
            self._cursor.execute( insert_site, self._message)
            self._conn.commit()
            messagebox.showinfo("注册站点", "注册站点成功")
        except:
            self._conn.rollback()
            messagebox.showerror("注册站点", "注册站点失败")
        finally:
            self._cursor.close()
            self._conn.close()

    def exist_site(self):
        select_site = "select siteid from siteinfor"
        exist_sitelist = []
        try :
            self._cursor.execute( select_site )
            exist_sitenum = self._cursor.fetchall()
            '''
            将读取到的数据库数据如：((1,), (2,), (3,), (5,), (6,), (7,))
            转换为列表形式[1, 2, 3, 5, 6, 7]
            '''
            for item in exist_sitenum:
                for i in item:
                    exist_sitelist.append(i)
            print(exist_sitelist)
            self._conn.commit()
            return exist_sitelist
        except:
            self._conn.rollbak()
        finally:
            self._cursor.close()
            self._conn.close()

    def drop_table(self, sitenumvar):
        delete_site = sitenumvar.get()
        tablename = "point%s"%delete_site
        tableavg24name = "point%s_avg24" % delete_site
        drop_site_sql = "delete from siteinfor where siteid=%s"
        drop_table_sql = "drop table %s"
        try :
            self._cursor.execute( drop_site_sql%delete_site )
            self._cursor.execute( drop_table_sql%tablename )
            self._cursor.execute( drop_table_sql %tableavg24name )
            self._conn.commit()
            messagebox.showinfo("撤销站点", "撤销站点成功")
        except:
            self._conn.rollbak()
            messagebox.showerror("撤销站点","撤销站点失败")
        finally:
            self._cursor.close()
            self._conn.close()