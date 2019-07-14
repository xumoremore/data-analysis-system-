from tkinter import *
from conn.connsql import ConnSql
import serial
import datetime
import time
from tkinter import messagebox
import threading
'''
class Conn(object):
    
    #*parameter表示接收任意多各参数并将其放在元祖中，所以site_list为一个元祖
    
    def __init__(self, conn_frame, ):
        self._conn_frame = conn_frame
 #       self._site_list = list(site_list)
        self._com_message = None
    def main_func(self):

        conn_look_site = ConnSql()
        sitenum_list = conn_look_site.exist_site()
        self.sitenumvar = StringVar()
        self.sitenumvar.set("选择站点")
        site_om = OptionMenu( self._conn_frame, self.sitenumvar, *sitenum_list)
        site_om.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.15)

        sqlbutton = Button( self._conn_frame, text="连接",
                            font=("华康少女字体", 20),
                            fg="black",
                            command=self.get_site).place(relx=0.5, rely=0.1, relwidth=0.3, relheight=0.15)

    def get_site(self):
        try:
            self.sitenum = self.sitenumvar.get()
            connsql = ConnSql()
            result = connsql.readdata(self.sitenum)
            print("获取到的数据为：%s"%result)
        except:
            print( "获取连接端口失败")
'''
'''
HEIGHT = 0.2
X = 0.1
Y = 0.1
INSTANCE_X = 0.05
INSTANCE_Y = 0.05
CONNMENU_HEIGHT = HEIGHT
COMMENU_HEIGHT =  HEIGHT
CONNBUTT_HEIGHT = HEIGHT
COMBUTT_HEIGHT = HEIGHT
CONNMENU_WIDTH =0.4
COMMENU_WIDTH = CONNMENU_WIDTH
CONNBUTT_WIDHT = 0.4
COMBUTT_WIDTH = CONNBUTT_WIDHT
CONNMENU_X = X
COMMENU_X =  X
CONNBUTT_X = X + CONNBUTT_WIDHT + INSTANCE_X
COMBUTT_X = X + COMMENU_WIDTH + INSTANCE_X
CONNMENU_Y = Y
COMMENU_Y = Y + COMMENU_HEIGHT + INSTANCE_Y
CONNBUTT_Y = Y
COMBUTT_Y = Y + CONNBUTT_HEIGHT + INSTANCE_Y
'''
class Uart(object):
    def __init__(self,conn_frame):
        self._conn_frame = conn_frame
        self._com_list = ["COM1", "COM2", "COM3", "COM4"]
    def main_func(self):
        # 接收的数据格式：“1+temp+air_humi+soil_humi+daily_rain"
        self._comvar = StringVar()
        self._comvar.set("选择串口")
        com_om = OptionMenu(self._conn_frame, self._comvar, *self._com_list)
        com_om.place(relx=0.01, rely=0.01, relwidth=0.3, relheight=0.23)

        combutton = Button(self._conn_frame, text="连接串口",
                           font=("华康少女字体", 20),
                           fg="black",
                           bg = 'steelblue',
                           command=self.conncom_button).place(relx=0.32, rely=0.01, relwidth=0.22, relheight=0.23)

        conn_look_site = ConnSql()
        sitenum_list = conn_look_site.exist_site()
        if sitenum_list == []:
            sitenum_list = ["数据库无站点信息"]
        sitenumvar = StringVar()
        sitenumvar.set("选择站点")
        site_om = OptionMenu(self._conn_frame, sitenumvar, *sitenum_list, )
        site_om.place(relx=0.01, rely=0.6, relwidth=0.3, relheight=0.23)

        #选择站点在这时候其实为发挥作用，通过选择的站点来获取数据库的信息得到要发送至该站点的gsm号码
        #然后重新设置gsm的at指令才能发送信息。通过调用get_gsm函数获得
        Button(self._conn_frame, text="开闸放水",
                           font=("华康少女字体", 20),
                           fg="black",
                           bg='steelblue',
                           command=self.openwater_button).place(relx=0.32, rely=0.6, relwidth=0.22, relheight=0.23)

        Label(self._conn_frame, text='ps上一条接收到的数据为：',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black").place(relx=0.57, rely=0.01, relwidth=0.4, relheight=0.2)

    def conncom_button(self):
        self.com_message = self._comvar.get()
        self._times = 0
        try:
            self.c_serial = serial.Serial(port=self.com_message, baudrate=9600, timeout=2)
            comopen = self.c_serial.isOpen()
            print("conopen的值为：%s" % comopen)
            messagebox.showinfo( "串口连接",self.com_message + "串口连接成功")
        except:
            try:
                self.c_serial.close()
                self.c_serial = serial.Serial(port=self.com_message, baudrate=9600, timeout=2)
                messagebox.showinfo("串口连接", self.com_message + "串口连接成功")
            except:
                messagebox.showerror("串口连接", self.com_message + "串口连接失败")
    def read_com(self,):
        try:
            timestr = time.strftime("%H:%M:%S")
            hour = str(timestr).split(':',1)[0]
            if str(timestr) == "23:30:00":    #在23：30分的时候进行该天数据的平均计算并且写入数据库
                avgsql = ConnSql()
                avgsql.read_avgdata()
        except:
            pass
        try:
            conwaiting = self.c_serial.inWaiting()
            if conwaiting:
                self.readdata = ''
                self.readdata = self.readdata.encode('utf-8')
                n = self.c_serial.inWaiting()
                self.readdata = self.readdata + self.c_serial.read(n)
                self.readdata = self.readdata.decode('gb18030')
                print( self.readdata )
                #将接收到的数据分割并且写入数据库，数据收发协议为：站点编号+数据。如：+1+20+20+20+20
                #由于在分割时会将+号前面的字符去掉，所以站点编号前需加多一个+号
                try :
                    readlist = self.readdata.split('+')
                    #使用生成数据：
                    if readlist[0] == '-':
                        timestr = str(self._times) + ":00:00"
                        self._times += 1
                        #datestr = "2019-05-02"
                        #datastr = datetime.date.today().strftime("%Y-%m-%d")
                        readlist.remove('-')
                    else:
                        timestr = time.strftime("%H:%M:%S")
                    datestr = datetime.date.today().strftime("%Y-%m-%d")
                    #datestr = "2019-07-14"
                    readlist.insert( 1, datestr )
                    readlist.insert( 2, timestr )
                    print("数据传入connsql成功为：")
                    self.recidata = "站点：" + readlist[0] + "\n" +"日期："+ readlist[1]  + "\n" + "时间：" + readlist[2] + "\n" \
                                   "温度：%s℃"%readlist[3] + "\n" + "空气湿度：%s"%readlist[4] + "%\n" + "土壤湿度：%s"%readlist[5] + "%\n" + "降雨量：%s"%readlist[6].strip() + "mL"
                    print(self.recidata)
                    recidatavar = StringVar()
                    recidatavar.set(self.recidata)
                    predicttext = Label(self._conn_frame, textvariable=recidatavar,
                                        font=("华康少女字体", 11),
                                        padx=0.5, pady=0.5,
                                        fg="black",bg='GhostWhite').place(relx=0.57, rely=0.21, relwidth=0.4, relheight=0.7)   #'MintCream' 'GhostWhite'
                    comsql = ConnSql()
                    comsql.writedata( comdata=readlist )
                except:
                    print("数据分割不成功")
        except:
            pass
        self._conn_frame.after(1000, self.read_com)   #必须要加这一句串口才能更新信息
    def openwater_button(self):
        OPEN = "1"
        try:
            if self.uartsend( OPEN ):
                messagebox.showinfo( "发送命令", "命令发送成功" )
        except:
            messagebox.showerror("发送命令", "命令发送失败")
    def get_gsm(self):
        pass

    def uartsend(self, command):
        sendstring = command
        sendstring = sendstring.encode('gb18030')
        self.c_serial.write(sendstring)
        print("串口发送命令")
        return True


