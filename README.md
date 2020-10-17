# 数据分析软件


## 目录
- [简介](#简介)
- [安装](#安装)
- [使用](#使用)

## 简介

该项目为本人的毕业设计，目的在于为森林环境监控提供数据记录-保存-分析-可视化的功能。软件主体采用python3开发；可视化界面使用tkinter框架；使用mysql做数据存储；使用逻辑回归算法对自己采集打标的数据做训练，预测环境数据所处的等级。

关键词：`数据分析` , `数据库`, `人脸识别` , `可视化界面`, 

## 安装

    pip install -r requirements.txt 

## 使用

运行代码：

    cd /data-analysis-system-
    python slws.py

### 目录结构

![目录结构](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/1.png)

### demo

下面链接为打包好的.exe可执行文件，可直接运行，但要使用数据库功能电脑需要安装mysql数据库。

可执行文件链接：[软件链接](https://pan.baidu.com/s/128nFX1aRHE8157biClGq8Q)

提取码：prto 

### 登录界面

    账号密码：root+root<br>
    人脸登陆功能，至对/face_recognition/face_data/me目录下的人物图片做为可登陆判断。
![Image text](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/3.png)

### 主界面

![Image text](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/4.png)

### 注册界面
![Image text](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/5.png)

### navicat for mysql软件里的senyan数据库界面
![Image text](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/6.png)

### 其中一个数据表
![Image text](https://github.com/xumoremore/data-analysis-system-/blob/master/introducepicture/7.png)
