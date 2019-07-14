from tkinter import *
import datetime
import time
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from infor.inforsql import InforSql
from sklearn import linear_model
import threading
date_time = datetime.datetime.now()

class Infor(object):
    FONT_TYPE = ("华康少女字体", 14)
    PADX = 5
    PADY = 10
    def __init__(self, infor_frame, site_frame, sqlsite, site_N, site_W, sqlpredict,):
        self._infor_frame = infor_frame    #可以不使用参数传入的方法也可以在infor_frame版块中添加控件
        self._sqlsite = sqlsite
        self._sqlplace = str( site_N ) + "N" + str( site_W ) + "W"
        self._sqlpredict = sqlpredict
        self._pred_all = 0
        self._site_frame = site_frame
    def main_func(self):

        '''
        在infor_frame的基础上创建标签框
        :return: 
        '''

        sitelabel = Label( self._site_frame, text="站点编号：",
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=0, column=0, sticky=W)
        self.sitevar = StringVar()
        self.sitevar.set( self._sqlsite )
        placelabel= Label( self._site_frame, textvariable=self.sitevar,
                            font = Infor.FONT_TYPE,
                            padx=Infor.PADX, pady=Infor.PADY,
                            fg = "black", bg = 'tan').grid(row=0, column=1, sticky=W)

        placelabel = Label( self._site_frame, text="地点：",
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=1, column=0, sticky=W)
        placevar = StringVar()
        placevar.set( self._sqlplace )
        placetext = Label( self._site_frame, textvariable=placevar,
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=1, column=1, sticky=W)

        timelabel = Label( self._site_frame, text="时间：",
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=3, column=0, sticky=W)
        datelabel = Label( self._site_frame, text="日期：",
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=2, column=0, sticky=W)
        '''
        调用after函数作为刷新，结果：无显示
                def time_refresh(self):
                    timevar = StringVar()
                    timevar.set( time.strftime("%H:%M:%S") )
                    timetext = Label( site_frame, textvariable=timevar,
                                       font = Infor.FONT_TYPE,
                                       padx=Infor.PADX, pady=Infor.PADY,
                                       fg = "black").grid(row=2, column=1, sticky=W)
                    self.after(10000,self.time_refresh)
        '''
        '''
        通过线程设置刷新时间，结果：无显示
        def time_refresh(self):
            global timer
            timer = threading.Timer(1, time_refresh )
            timer.start()
            timevar.set(  datetime.datetime.now() )
        timer = threading.Timer(1,time_refresh)
        timer.start
        '''
        print("向infor写入信息")

        def time_refresh():
            datestr = datetime.date.today().strftime("%Y-%m-%d")
            timestr = time.strftime("%H:%M:%S")
            datetext.configure(text=datestr)
            timetext.configure(text=timestr)
            self._site_frame.after( 1000, time_refresh )
        #将time_refresh()放在这里程序执行不了
        timetext = Label(self._site_frame, text='',
                         font=Infor.FONT_TYPE,
                         padx=Infor.PADX, pady=Infor.PADY,
                         fg="black", bg = 'tan')
        timetext.grid(row=3, column=1, sticky=W)
        datetext = Label(self._site_frame, text='',
                         font=Infor.FONT_TYPE,
                         padx=Infor.PADX, pady=Infor.PADY,
                         fg="black", bg = 'tan')
        datetext.grid(row=2, column=1, sticky=W)
        time_refresh()  # 将time_refresh()放在这里程序执行正确

        predictlabel = Label( self._site_frame, text="预警：",
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=4, column=0, sticky=W)
        predictvar = StringVar()
        predictvar.set( self._sqlpredict )
        predicttext = Label( self._site_frame, textvariable=predictvar,
                           font = Infor.FONT_TYPE,
                           padx=Infor.PADX, pady=Infor.PADY,
                           fg = "black", bg = 'tan').grid(row=4, column=1, sticky=W)
        print("向infor写入信息")
        #显示warning_infor标签
        Label( self._site_frame, text="当前温度状况：",
               font = Infor.FONT_TYPE,
               padx=Infor.PADX, pady=Infor.PADY,
               fg = "black", bg = 'tan').grid(row=0, column=2, sticky=W)
        Label( self._site_frame, text="当前空气湿度状况：",
               font = Infor.FONT_TYPE,
               padx=Infor.PADX, pady=Infor.PADY,
               fg = "black", bg = 'tan').grid(row=1, column=2, sticky=W)
        Label( self._site_frame, text="当前土壤湿度状况：",
               font = Infor.FONT_TYPE,
               padx=Infor.PADX, pady=Infor.PADY,
               fg = "black", bg = 'tan').grid(row=2, column=2, sticky=W)
        Label( self._site_frame, text="当前降雨量状况：",
               font = Infor.FONT_TYPE,
               padx=Infor.PADX, pady=Infor.PADY,
               fg = "black", bg = 'tan').grid(row=3, column=2, sticky=W)
        Label( self._site_frame, text="整体环境状况：",
               font = Infor.FONT_TYPE,
               padx=Infor.PADX, pady=Infor.PADY,
               fg = "black", bg = 'tan').grid(row=4, column=2, sticky=W)




class PredictInfor():
    def __init__(self, sitenum, site_frame):
        self._sitenum = sitenum
        self._site_frame = site_frame
    def warning_infor(self):
        pred_all = 0
        pred_temp, pred_airhumi, pred_soilhumi, pred_dailyrain = self.predict()
        print("pred_temp的值为：%s"%pred_temp)
        warning = ['下图','良好', '正常', '一般', '超标', '严重超标']
        #             1        2       3       4          5
        warning_color = ['black','green', 'blue', 'yellow', 'Orange', 'red']
        tempvar = StringVar()
        tempvar.set(warning[pred_temp])
        temptext = Label(self._site_frame, textvariable=tempvar,
                         font=Infor.FONT_TYPE,
                         padx=Infor.PADX, pady=Infor.PADY,
                         fg=warning_color[pred_temp], bg='tan').grid(row=0, column=3, sticky=W)

        airhumivar = StringVar()
        airhumivar.set(warning[pred_airhumi])
        airhumitext = Label(self._site_frame, textvariable=airhumivar,
                            font=Infor.FONT_TYPE,
                            padx=Infor.PADX, pady=Infor.PADY,
                            fg=warning_color[pred_airhumi], bg='tan').grid(row=1, column=3, sticky=W)

        soilhumivar = StringVar()
        soilhumivar.set(warning[pred_soilhumi])
        soilhumitext = Label(self._site_frame, textvariable=soilhumivar,
                             font=Infor.FONT_TYPE,
                             padx=Infor.PADX, pady=Infor.PADY,
                             fg=warning_color[pred_soilhumi], bg='tan').grid(row=2, column=3, sticky=W)

        dailyrainvar = StringVar()
        dailyrainvar.set(warning[pred_dailyrain])
        dailyraintext = Label(self._site_frame, textvariable=dailyrainvar,
                              font=Infor.FONT_TYPE,
                              padx=Infor.PADX, pady=Infor.PADY,
                              fg=warning_color[pred_dailyrain], bg='tan').grid(row=3, column=3, sticky=W)

        predallvar = StringVar()
        predallvar.set(warning[pred_all])
        temptext = Label(self._site_frame, textvariable=predallvar,
                         font=Infor.FONT_TYPE,
                         padx=Infor.PADX, pady=Infor.PADY,
                         fg=warning_color[pred_all], bg='tan').grid(row=4, column=3, sticky=W)
        #           site_frame.after(1, warning_infor )

    def predict(self):
        x_temp, x_air_humi, x_soil_humi, x_daily_rain = self.loadset()
        x_temp = np.array(x_temp)
        print("x_temp的值为:%s"%x_temp)
        x_temp.reshape(-1,1)
        print(x_temp)
        x_air_humi = np.array(x_air_humi)
        x_air_humi.reshape(-1,1)

        x_soil_humi = np.array(x_soil_humi)
        x_soil_humi.reshape(-1,1)
        x_daily_rain = np.array(x_daily_rain)
        x_daily_rain.reshape(-1,1)
        # print("x_data的值为：%s"%x_data)
        # x_temp=np.array(x_data[0]).reshape(-1,1)
        # x_air_humi=np.array(x_data[1]).reshape(-1,1)
        # x_soil_humi=np.array(x_data[2]).reshape(-1,1)
        # x_daily_rain=np.array(x_data[3]).reshape(-1,1)

        # 温度输出为1的样例[30, 30, 27, 35, 33, 25, 27, 33, 33, 29, 30, 28, 35, 27, 31, 30, 31, 35, 32, 33, 26, 27, 25, 28]
        # 温度输出为5的样例[10, 5, 6, 9, 8, 6, 10, 8, 7, 6, 5, 6, 9, 10, 10, 6, 10, 7, 8, 7, 9, 6, 5, 7]
        # output1 = np.array(
        #     [30, 30, 27, 31, 33, 25, 27, 30, 33, 29, 30, 25, 35, 27, 31, 30, 35, 35, 32, 33, 26, 27, 25, 28])
        # output1.reshape(-1, 1)
        # output5 = np.array([10, 5, 6, 9, 8, 6, 10, 8, 7, 6, 5, 6, 9, 10, 10, 6, 10, 7, 8, 7, 9, 6, 5, 7])
        # output5.reshape(-1, 1)
#该路径必须为绝对路径，并且不能含有中文
        model_temp = joblib.load('D:/senyan24/infor/model/model_temp.pkl')
        pred_temp = model_temp.predict(x_temp)

        print(x_air_humi)
        model_air_humi = joblib.load('D:/senyan24/infor/model/model_air_humi.pkl')
        pred_airhumi = model_air_humi.predict(x_air_humi)
        print(pred_airhumi)

        model_soil_humi = joblib.load('D:/senyan24/infor/model/model_soil_humi.pkl')
        pred_soilhumi = model_soil_humi.predict(x_soil_humi)

        model_daily_rain = joblib.load('D:/senyan24/infor/model/model_daily_rain.pkl')
        pred_dailyrain = model_daily_rain.predict(x_daily_rain)

        if pred_temp>5:
            pred_temp = 5
        if pred_airhumi>5:

            pred_airhumi=5
        if pred_soilhumi>5:
            pred_soilhumi = 5
        if pred_dailyrain>5:
            pred_dailyrain=5
        return int(pred_temp), int(pred_airhumi), int(pred_soilhumi), int(pred_dailyrain)

    def loadset(self):
        predictsql = InforSql()
        data = predictsql.readpredict( self._sitenum )
        print(len(data))
        # 读取下来的数据格式  ((30, 68, 69, 2), (30, 68, 67, 8), (27, 75, 74, 6), (35, 70, 73, 9),
        # (33, 73, 66, 4), (25, 66, 67, 6), (27, 75, 72, 10), (33, 72, 73, 7), (33, 72, 70, 1))
        x_temp = []
        x_air_humi = []
        x_soil_humi = []
        x_daily_rain = []

        oneday_xtemp = []
        oneday_xair_humi = []
        oneday_xsoil_humi = []
        oneday_xdaily_rain = []
        for index in range(len(data)):
            oneday_xtemp.append(data[index][0])
            oneday_xair_humi.append(data[index][1])
            oneday_xsoil_humi.append(data[index][2])
            oneday_xdaily_rain.append(data[index][3])

        print('处理前的数据%s' % oneday_xtemp)
        oneday_xtemp = self.fillnone(oneday_xtemp)
        oneday_xair_humi = self.fillnone(oneday_xair_humi)
        oneday_xsoil_humi = self.fillnone(oneday_xsoil_humi)
        oneday_xdaily_rain = self.fillnone(oneday_xdaily_rain)

        x_temp.append(oneday_xtemp)
        x_air_humi.append(oneday_xair_humi)
        x_soil_humi.append(oneday_xsoil_humi)
        x_daily_rain.append(oneday_xdaily_rain)
        print('处理过后的数据%s' % oneday_xtemp)

        return x_temp, x_air_humi, x_soil_humi, x_daily_rain

    def fillnone(self, listdata):
        print("输入的listdata为%s"%listdata)
        data = pd.DataFrame(listdata)
        data = data.fillna(1)
        data = np.array(data)
        data = data.reshape(1, -1)
        data = data[0]
        return_listdata = data.tolist()
        print("补全数据前的长度为：%s"%len(return_listdata))
        lacknum = 24 - len(return_listdata)
        if lacknum != 0:
            for n in range(lacknum):
                return_listdata.append(1)
        print("补全之后的数据%s"%return_listdata)
        return return_listdata
#气象预警信号，一般都有蓝、黄、橙、红四种颜色等级

# class warning_infor(object):
#     def __init__(self, site_frame, pred_temp, pred_airhumi, pred_soilhumi, pred_dailyrain):
#
#         self._pred_temp = pred_temp
#         self._pred_airhumi = pred_airhumi
#         self._pred_soilhumi = pred_soilhumi
#         self._pred_dailyrain = pred_dailyrain
#     def main_func(self):

