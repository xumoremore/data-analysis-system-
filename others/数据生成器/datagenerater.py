import numpy as np
import datetime
import time
import pymysql
import serial
import threading
class DataGenerater(object):
    def __init__(self, site, comnum):
        self._site = str(site)
        self._comnum = comnum
        self._data = [0,0,0,0]
        self._conn = pymysql.connect(host="localhost",
                               user="root",
                               password="xuzhenchu",
                               database="senyan")
        self._cursor = self._conn.cursor()

    def genedata(self):
        #self._data[0] = datetime.date.today().strftime("%Y-%m-%d")
        #self._data[1] = time.strftime("%H:%M:%S")
        self._datastr = self._site
        self._data[0] = np.random.random_integers( 5, 10, 1).tolist()   #温度
        self._data[1] = np.random.random_integers(45, 55, 1).tolist()    #空气湿度
        self._data[2] = np.random.random_integers( 45, 55, 1).tolist()   #土壤湿度
        self._data[3] = np.random.random_integers( 100, 250, 1).tolist()   #日降雨量
        print(self._data)
        for i in self._data:
            for y in i:
                self._datastr = self._datastr + "+" + str(y)
        self._datastr = '-+' + self._datastr
        print(self._datastr)
        return self._datastr
    def senddata(self):
        self.com_message = self._comnum
        try:
            self.c_serial = serial.Serial(port=self.com_message, baudrate=9600, timeout=2)
            comopen = self.c_serial.isOpen()
            print("conopen的值为：%s" % comopen)
            print("串口连接", self.com_message + "串口连接成功")
        except:
            print("串口连接", self.com_message + "串口连接成功")
        sendstring = self.genedata()
        sendstring = sendstring.encode('gb18030')
        self.c_serial.write(sendstring)



timestrlist = []
timelist =[]
count = 0
def fast_main( site, comnum):
    conn = pymysql.connect(host="localhost",
                                 user="root",
                                 password="xuzhenchu",
                                 database="senyan")
    cursor = conn.cursor()
    times = 0
    timestr = time.strftime("%H:%M:%S")
    while times!=24:
        if timestr != time.strftime("%H:%M:%S"):
            print(times)
            timestrlist.append(timestr)
            timelist = time.time()
            print(time.time())
            times += 1
            datagenerater = DataGenerater( site=site, comnum=comnum)
            datagenerater.senddata()
            timestr = time.strftime("%H:%M:%S")
            time.sleep(2)


if __name__ == "__main__":
    fast_main( site=3, comnum="COM2")   #向COM2串口发送生成的站点4数据

