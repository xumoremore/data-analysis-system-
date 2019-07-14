from tkinter import *
import datetime
from graph.graphsql import GraphSql
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
from sklearn.externals import joblib
import matplotlib.pyplot as plt


class Graph(object):
    def __init__(self, graph_frame, sitenum):
        self._graph_frame = graph_frame
        self._temptime = []
        self._temp = []
        self._airhumitime = []
        self._airhumi = []
        self._soilhumitime = []
        self._soilhumi = []
        self._dailyraintime = []
        self._dailyrain = []
        self._sitenum = str(sitenum)
    def main_func(self):

        #timedelta可以通过day属性获取天数，这个天数就是int型了

        '''
        获取温度数据并在绘图布上显示
        
        templabel = Label(self._graph_frame, text='温度 ℃/小时',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black", bg="white").place(relx=0.15, rely=0, relwidth=0.2, relheight=0.05)
        soilhumilabel = Label(self._graph_frame, text='空气湿度 %/小时',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black", bg="white").place(relx=0.65, rely=0, relwidth=0.2, relheight=0.05)
        soilhumilabel = Label(self._graph_frame, text='土壤湿度 %/小时',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black", bg="white").place(relx=0.15, rely=0.5, relwidth=0.2, relheight=0.05)
        dailyrainlabel = Label(self._graph_frame, text='日降雨量 ml/小时',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black", bg="white").place(relx=0.65, rely=0.5, relwidth=0.2, relheight=0.05)
        '''
        tempsql = GraphSql()
        tempdata = tempsql.readdata( sitenum=self._sitenum, dataname="temp" )
        print(tempdata)
        for time, temp in tempdata:
            temphour = str(time).split(':',1)[0]   #分割00：00：00类型的数据并且提取第一个元素hour
            self._temptime.append(temphour)
            self._temp.append(temp)
        print(self._temptime)
        print( "获取到的温度数据为：")
        print( tempdata )
        temp_f = Figure(figsize=(3.5, 3), dpi=100, facecolor='aliceblue')    #figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)
        temp = temp_f.add_subplot(111)  # 添加子图:1行1列第1个

        temp.set_xlabel('H')
        temp.set_ylabel('temp')
        temp.set_ylim((0, 50))
        temp.set_xlim((0, 24))
        temp.yaxis.set_minor_locator(MultipleLocator(5))  # 设置y轴小刻度
        temp.yaxis.set_major_locator(MultipleLocator(10))
        # 在值横坐标虚线
        temp.grid(True, which='minor', axis='y', c='c', linestyle='-.', linewidth=0.2)

        #temp.get_xaxis().set_visible(True)  # 关闭横坐标
        temp.spines['right'].set_visible(False)  # 关闭轴
        # a.xaxis.set_ticks_position('top')      #将下轴向上颠倒
        temp.spines['top'].set_position(('data', 0))  # 去掉上右两个轴
        print("temp曲线图执行标记1:temp的值%s"%self._temp)
        print("temptime的值%s"%self._temptime)
        # 生成用于绘sin图的数据
        temp.plot( self._temptime,  self._temp,  )
        print("temp曲线图执行标记2")
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        temp_canvas = FigureCanvasTkAgg(temp_f, master=self._graph_frame)
        temp_canvas.draw()  # 注意show方法已经过时了,这里改用draw
        temp_canvas.get_tk_widget().place( relx=0, rely=0, relwidth=0.49, relheight=0.5 ) # 随窗口大小调整而调整

        '''
        获取空气湿度数据并在绘图布上显示
        '''
        airhumisql = GraphSql()
        airhumidata = airhumisql.readdata(sitenum=self._sitenum, dataname="air_humi")
        for time, airhumi in airhumidata:
            airhumihour = str(time).split(':',1)[0]   #分割00：00：00类型的数据并且提取第一个元素hour
            self._airhumitime.append(airhumihour)
            self._airhumi.append(airhumi)
        print( self._airhumitime )
        print(self._airhumi)
        f_airhumi = Figure(figsize=(3, 2.5), dpi=100, facecolor='aliceblue')  # 茶色，figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)
        airhumi = f_airhumi.add_subplot(111)  # 添加子图:1行1列第1个
        airhumi.set_xlabel('H')
        airhumi.set_ylabel('air humity %')
        airhumi.set_ylim((0, 100))
        airhumi.set_xlim((0, 24))
        airhumi.yaxis.set_minor_locator(MultipleLocator(10))  # 设置y轴小刻度
        airhumi.yaxis.set_major_locator(MultipleLocator(10))
        # 在值横坐标虚线
        airhumi.grid(True, which='minor', axis='y', c='c', linestyle='-.', linewidth=0.2)
        #airhumi.get_xaxis().set_visible(True)  # 关闭横坐标
        airhumi.spines['right'].set_visible(False)  # 关闭轴
        # airhumi.xaxis.set_ticks_position('top')      #将下轴向上颠倒
        airhumi.spines['top'].set_position(('data', 0))  # 去掉上右两个轴

        airhumi.plot(self._airhumitime, self._airhumi )
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        air_canvas = FigureCanvasTkAgg( f_airhumi, master=self._graph_frame)
        air_canvas.draw()  # 注意show方法已经过时了,这里改用draw
        air_canvas.get_tk_widget().place( relx=0.5, rely=0, relwidth=0.49, relheight=0.5 )  # 随窗口大小调整而调整

        '''
        获取土壤湿度数据并在绘图布上显示
        '''
        soilhumisql = GraphSql()
        soilhumidata = soilhumisql.readdata(sitenum=self._sitenum, dataname="soil_humi")
        for time, soilhumi in soilhumidata:
            soilhumihour = str(time).split(':',1)[0]   #分割00：00：00类型的数据并且提取第一个元素hour
            self._soilhumitime.append(soilhumihour)
            self._soilhumi.append(soilhumi)
        f_soilhumi = Figure(figsize=(3, 2.5), dpi=100,facecolor='aliceblue')    #figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)
        soilhumi = f_soilhumi.add_subplot(111)  # 添加子图:1行1列第1个

        soilhumi.set_xlabel('H')
        soilhumi.set_ylabel('soil humity %')
        soilhumi.set_ylim((0, 100))
        soilhumi.set_xlim((0, 24))
        soilhumi.yaxis.set_minor_locator(MultipleLocator(10))  # 设置y轴小刻度
        soilhumi.yaxis.set_major_locator(MultipleLocator(10))
        # 在值横坐标虚线
        soilhumi.grid(True, which='minor', axis='y', c='c', linestyle='-.', linewidth=0.2)
        #airhumi.get_xaxis().set_visible(True)  # 关闭横坐标
        soilhumi.spines['right'].set_visible(False)  # 关闭轴
        # airhumi.xaxis.set_ticks_position('top')      #将下轴向上颠倒
        soilhumi.spines['top'].set_position(('data', 0))  # 去掉上右两个轴

        soilhumi.plot(self._soilhumitime, self._soilhumi)
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        soilhumi_canvas = FigureCanvasTkAgg(f_soilhumi, master=self._graph_frame)
        soilhumi_canvas.draw()  # 注意show方法已经过时了,这里改用draw
        soilhumi_canvas.get_tk_widget().place( relx=0, rely=0.5, relwidth=0.49, relheight=0.5) # 随窗口大小调整而调整

        '''
        获取日降雨量数据并在绘图布上显示
        '''
        dailyrainsql = GraphSql()
        dailyraindata = dailyrainsql.readdata(sitenum=self._sitenum, dataname="daily_rain")
        for time, dailyrain in dailyraindata:
            dailyrainhour = str(time).split(':',1)[0]   #分割00：00：00类型的数据并且提取第一个元素hour
            self._dailyraintime.append(dailyrainhour)
            self._dailyrain.append(dailyrain)
        print("日降雨量")
        print(self._dailyraintime)
        print(self._dailyrain)
        f_dailyrain = Figure(figsize=(3, 2.5), dpi=100,facecolor='aliceblue')  # figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)
        dailyrain = f_dailyrain.add_subplot(111)  # 添加子图:1行1列第1个
        dailyrain.set_xlabel('H')
        dailyrain.set_ylabel('daily rainfull mL')
        dailyrain.set_ylim((0, 500))
        dailyrain.set_xlim((0, 24))
        dailyrain.yaxis.set_minor_locator(MultipleLocator(50))  # 设置y轴小刻度
        dailyrain.yaxis.set_major_locator(MultipleLocator(100))
        # 在值横坐标虚线
        dailyrain.grid(True, which='minor', axis='y', c='c', linestyle='-.', linewidth=0.2)
        #airhumi.get_xaxis().set_visible(True)  # 关闭横坐标
        dailyrain.spines['right'].set_visible(False)  # 关闭轴
        # airhumi.xaxis.set_ticks_position('top')      #将下轴向上颠倒
        dailyrain.spines['top'].set_position(('data', 0))  # 去掉上右两个轴

        dailyrain.plot(self._dailyraintime, self._dailyrain)
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        dailyrain_canvas = FigureCanvasTkAgg(f_dailyrain, master=self._graph_frame)
        dailyrain_canvas.draw()  # 注意show方法已经过时了,这里改用draw

        dailyrain_canvas.get_tk_widget().place( relx=0.5, rely=0.5, relwidth=0.49, relheight=0.5 )  # 随窗口大小调整而调整

class PredictGraph(object):
    def __init__(self, infor_frame, sitenum):
        self._infor_frame = infor_frame
        self._sitenum = str(sitenum)
        self._alltime = []
        self._all = []
    def main_func(self):
        print("predict调用")
        print("predict sitenum:%s" % self._sitenum)
        allsql = GraphSql()
        alldata = allsql.readall(sitenum=self._sitenum)

        templabel = Label(self._infor_frame, text='数据分析曲线',
                            font=("华康少女字体", 12),
                            padx=0.5, pady=0.5,
                            fg="black", bg="white").place(relx=0.3, rely=0.5, relwidth=0.3, relheight=0.05)
        print("获取到的所有数据为%s")
        print(alldata)
        for time, temp, airhumi, soilhumi, dailyrain in alldata:
            allhour = str(time).split(':', 1)[0]  # 分割00：00：00类型的数据并且提取第一个元素hour
            self._alltime.append(allhour)
            alldata = temp+airhumi+soilhumi+dailyrain
            datalist = [temp,airhumi,soilhumi,dailyrain]
            predictdata = self.graphpredict( datalist )
            self._all.append(int(predictdata))
            print("获取到的datalist为：")
            print(datalist)
        print(self._all)
        predict_f = Figure(figsize=(3, 2.5), dpi=100,facecolor='GhostWhite')  # figsize:以英寸为单位的宽高，缺省值为 rc figure.figsize (1英寸等于2.54厘米)
        predict = predict_f.add_subplot(111)  # 添加子图:1行1列第1个
        predict.set_xlabel('time')
        predict.set_ylabel('warning')
        predict.set_ylim((0, 8))
        predict.set_xlim((0, 24))
        predict.yaxis.set_minor_locator(MultipleLocator(5))  # 设置y轴小刻度
        predict.yaxis.set_major_locator(MultipleLocator(10))
        # 在值横坐标虚线
        predict.grid(True, which='minor', axis='y', c='c', linestyle='-.', linewidth=0.2)
        #airhumi.get_xaxis().set_visible(True)  # 关闭横坐标
        predict.spines['right'].set_visible(False)  # 关闭轴
        # airhumi.xaxis.set_ticks_position('top')      #将下轴向上颠倒
        predict.spines['top'].set_position(('data', 0))  # 去掉上右两个轴
        # 生成用于绘sin图的数据
        # predict.plot(self._alltime, self._all, )
        predict.scatter(self._alltime, self._all, )
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        all_canvas = FigureCanvasTkAgg(predict_f, master=self._infor_frame)
        all_canvas.draw()  # 注意show方法已经过时了,这里改用draw
        all_canvas.get_tk_widget().place( relx=0, rely=0.55, relwidth=1, relheight=0.45 )
        #all_canvas.get_tk_widget().grid(row=1, column=0)  # 随窗口大小调整而调整

    def graphpredict(self,*datalist):
        data = datalist
        model_graph = joblib.load("D:/senyan24/graph/model/model_graph.pkl")
        result = model_graph.predict(data)
        print(result)
        return result

