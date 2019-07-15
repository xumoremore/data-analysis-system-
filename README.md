森林卫士
====
主要用到的python库：tkinter，pymysql，numpy，opencv，matplotlib，pandas，sklearn，os，sys，serial，time
软件整体代码结构
-----
除了others目录和dist目录（dist目录为软件打包为.exe格式用来存放该应用程序的目录）的文件，其他的包都会被slws.py文件调用。

![add image](https://github.com/xumoremore/data-analysis-system-/tree/master/introducepicture/1.png)

others目录里的文件：
----
Predict：用于训练数据分析模型
数据生成器：用于模拟下位机硬件向软件发送数据

登录界面
-----
可使用账号+密码登录：root+root
也可以使用人脸一键登录：当然该软件只能通过本人的人脸进行登录（因为里面只有我的人脸数据）

主界面
----

注册界面
-----

navicat for mysql软件里的senyan数据库界面
----

表point3数据
-----
不要问表为什么这么整齐，因为是使用数据生成器生成的


![Image text](https://github.com/xumoremore/data-analysis-system-/tree/master/introducepicture/1.png)
