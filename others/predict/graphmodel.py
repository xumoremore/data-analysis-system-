from sklearn.linear_model import LinearRegression
from predict.predictsql import PredictSql
from sklearn.externals import joblib
import numpy as np
import pandas as pd
class GraphModel():
    def __init(self):
        pass

    def loadset(self):
        train_x = []
        train_y = []
        dataset = pd.read_csv("D:/senyan24/predict/graph_traindata.csv")
        dataset = np.array(dataset).tolist()
        for onedata in dataset:
            y_data = onedata.pop()  #移除并返回列表最后一个元素
            train_y.append(y_data)
            train_x.append(onedata)
        print(train_x, train_y, )
        return train_x, train_y

    def trainmodel(self):
        self.model_graph= LinearRegression()
        x_data, y_data = self.loadset()
        self.model_graph.fit( x_data, y_data)
        joblib.dump(self.model_graph, 'model/model_graph.pkl')



if __name__ ==  "__main__":
    # graphmodel = GraphModel()
    # graphmodel.trainmodel()
    model_graph = joblib.load('model/model_graph.pkl')
    test = [33, 73, 66, 4]
    test = np.array(test)
    test.reshape(-1,1)
    result = model_graph.predict(test)
    print(result)