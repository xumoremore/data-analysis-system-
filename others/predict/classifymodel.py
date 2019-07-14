from sklearn.linear_model import LinearRegression
from predict.predictsql import PredictSql
from sklearn.externals import joblib
import numpy as np
import pandas as pd
class ClassifyModel():
    def __init(self):
        pass

    def loadset(self):
        predictsql = PredictSql()
        data = predictsql.readall( sitenum='0' )
        print( len(data) )
        #读取下来的数据格式  ((30, 68, 69, 2), (30, 68, 67, 8), (27, 75, 74, 6), (35, 70, 73, 9),
        # (33, 73, 66, 4), (25, 66, 67, 6), (27, 75, 72, 10), (33, 72, 73, 7), (33, 72, 70, 1))
        x_temp=[]
        x_air_humi=[]
        x_soil_humi=[]
        x_daily_rain=[]

        oneday_xtemp=[]
        oneday_xair_humi=[]
        oneday_xsoil_humi=[]
        oneday_xdaily_rain=[]

        y_temp=[]
        y_air_humi=[]
        y_soil_humi=[]
        y_daily_rain=[]
        for index in range( len(data) ):
            if (index+1)%25 == 0:
                y_temp.append( data[index][0])
                y_air_humi.append( data[index][1])
                y_soil_humi.append( data[index][2])
                y_daily_rain.append( data[index][3])
                print('处理前的数据%s' % oneday_xtemp)
                oneday_xtemp = self.fillnone(oneday_xtemp)
                oneday_xair_humi = self.fillnone(oneday_xair_humi)
                oneday_xsoil_humi = self.fillnone(oneday_xsoil_humi)
                oneday_xdaily_rain = self.fillnone(oneday_xdaily_rain)

                x_temp.append( oneday_xtemp)
                x_air_humi.append( oneday_xair_humi)
                x_soil_humi.append( oneday_xsoil_humi)
                x_daily_rain.append( oneday_xdaily_rain)
                print('处理过后的数据%s'%oneday_xtemp)
                oneday_xtemp = []
                oneday_xair_humi = []
                oneday_xsoil_humi = []
                oneday_xdaily_rain = []
                continue;
            oneday_xtemp.append( data[index][0] )
            oneday_xair_humi.append( data[index][1] )
            oneday_xsoil_humi.append( data[index][2] )
            oneday_xdaily_rain.append( data[index][3] )

        print(x_temp,y_temp)
        return (  x_temp, x_air_humi, x_soil_humi, x_daily_rain,),\
               (  y_temp,  y_air_humi,  y_soil_humi,  y_daily_rain,)
    def fillnone(self, listdata):
        data = pd.DataFrame( listdata )
        data = data.fillna(1)
        data = np.array(data)
        data = data.reshape(1,-1)
        data = data[0]
        return_listdata = data.tolist()
        return return_listdata

    def trainmodel(self):
        self.model_temp= LinearRegression()
        self.model_air_humi= LinearRegression()
        self.model_soil_humi= LinearRegression()
        self.model_daily_rain= LinearRegression()

        x_data, y_data = self.loadset()
        x_temp=x_data[0]
        x_air_humi=x_data[1]
        x_soil_humi=x_data[2]
        x_daily_rain=x_data[3]
        y_temp=y_data[0]
        y_air_humi=y_data[1]
        y_soil_humi=y_data[2]
        y_daily_rain=y_data[3]

        self.model_temp.fit( x_temp, y_temp)
        joblib.dump(self.model_temp, 'model/model_temp.pkl')
        self.model_air_humi.fit( x_air_humi, y_air_humi )
        joblib.dump(self.model_air_humi, 'model/model_air_humi.pkl')
        self.model_soil_humi.fit( x_soil_humi, y_soil_humi )
        joblib.dump(self.model_soil_humi, 'model/model_soil_humi.pkl')
        self.model_daily_rain.fit( x_daily_rain, y_daily_rain )
        joblib.dump(self.model_daily_rain, 'model/model_daily_rain.pkl')


if __name__ ==  "__main__":
    # classifymodel = ClassifyModel()
    # classifymodel.trainmodel()
    model_temp = joblib.load('model/model_air_humi.pkl')
    #温度输出为1的样例[30, 30, 27, 35, 33, 25, 27, 33, 33, 29, 30, 28, 35, 27, 31, 30, 31, 35, 32, 33, 26, 27, 25, 28]
    #温度输出为5的样例[10, 5, 6, 9, 8, 6, 10, 8, 7, 6, 5, 6, 9, 10, 10, 6, 10, 7, 8, 7, 9, 6, 5, 7]
    output1 = np.array([30, 30, 27, 31, 33, 25, 27, 30, 33, 29, 30, 25, 35, 27, 31, 30, 35, 35, 32, 33, 26, 27, 25, 28])
    output1.reshape(-1,1)
    output5 = np.array([46, 45, 45, 45, 51, 51, 51, 52, 53, 54, 55, 51, 52, 53, 54, 52, 54, 46, 45, 45, 45, 45, 46, 47])
    output5.reshape(-1,1)
    result = model_temp.predict(output5)
    print( result[0] )