from tkinter import *
#from conn.conn import Conn
from conn.connsql import ConnSql
from conn.conn import Uart
from infor.infor import Infor
from register.register import Register
from graph.graph import Graph,PredictGraph
from topmenu.topmenu import TopMenu
import threading
from tkinter import messagebox
from face_recognition.video_face_recognition import face_rec
from infor.infor import PredictInfor
import time
#from __init__ import *

ROOT_HEIGHT = 800
ROOT_WIDTH = 1400
DISPLAY_RATE_ROOT = 0.7     #display_frame和control_frame框高度的比值， DISPLAY_RATE_CONTROL =  展示框高度/root框高度
PLOT_RATE_ROOT = 0.65         #plot_frame和display_frame框宽度的比值， PLOT_RATE_INFOR = 数据显示框宽度/root框宽度
REGISTER_RATE_ROOT = 0.45    #register_frame和control_frame框宽度的比值，REGISTER_RATE_CONN = 注册框宽度/root框宽度

'''
分是个窗体并且设置其大小

----0.7------------------------------
|                      |            |
 0.6 数据显示框         |  信息框    |      上部分为展示框
|                      |            |   
--------------------------------------                               总体为root框
|              |                     |      
|  注册框      |     连接框          |     下部分为控制框
|              |                     |  
----0.4------------------------------    
'''

DISPLAY_HEIGHT = DISPLAY_RATE_ROOT * ROOT_HEIGHT
DISPLAY_WIDTH = ROOT_WIDTH

PLOT_HEIGHT = DISPLAY_HEIGHT
PLOT_WIDTH = PLOT_RATE_ROOT * DISPLAY_WIDTH
INFOR_HEIGHT = DISPLAY_HEIGHT
INFOR_WIDTH = (1-PLOT_RATE_ROOT) * DISPLAY_WIDTH

CONTROL_HEIGHT = (1-DISPLAY_RATE_ROOT) * ROOT_HEIGHT   #下面控制窗口的展示框架高度为300
CONTROL_WIDTH = ROOT_WIDTH

REGISTER_HEIGHT = DISPLAY_HEIGHT
REGISTER_WIDTH = REGISTER_RATE_ROOT * CONTROL_WIDTH
CONN_HEIGHT = CONTROL_HEIGHT
CONN_WIDTH = (1-REGISTER_RATE_ROOT) * CONTROL_WIDTH

root = Tk()
root.title("森眼—森林卫士")
#root.geometry("1000x800")

class SenlinWeiShi():
    def __init__(self):
        self.display_frame = Frame(root, height=DISPLAY_HEIGHT, width=DISPLAY_WIDTH, )
        self.control_frame = Frame(root, height=CONTROL_HEIGHT, width=CONTROL_WIDTH, )
        self.graph_frame = Frame(self.display_frame, bg="white", height=PLOT_HEIGHT, width=PLOT_WIDTH, )
        self.infor_frame = Frame(self.display_frame, bg='white', height=INFOR_HEIGHT, width=INFOR_WIDTH, )
        self.register_frame = Frame(self.control_frame, bg="white", height=REGISTER_HEIGHT, width=REGISTER_WIDTH, )
        self.conn_frame = LabelFrame(self.control_frame, text="连接", font=("华康少女字体", 20), bg='white', height=CONN_HEIGHT,
                                width=CONN_WIDTH, padx=5, pady=5)
        self.site_frame = LabelFrame(self.infor_frame, text="站点信息", font=("华康少女字体", 20), bg='tan', width=400, height=400,
                                padx=5, pady=5)
    def main(self):
        '''
        连接按钮控制数据显示界面连接的数据库信息显示
        :return: 
        '''
        conn_look_site = ConnSql()
        sitenum_list = conn_look_site.exist_site()
        if sitenum_list == []:
            sitenum_list = ["数据库无站点信息"]
        self.sitenumvar = StringVar()
        self.sitenumvar.set("选择站点")
        print("选择站点执行")
        site_om = OptionMenu(self.conn_frame, self.sitenumvar, *sitenum_list, )
        site_om.place(relx=0.01, rely=0.3, relwidth=0.3, relheight=0.23)



        topmenu = TopMenu( frame = root )
        topmenu.main_func()
        register = Register(register_frame=self.register_frame, graph_frame=self.graph_frame )  #
        message = register.main_func()

        # pack_propagate(0)是使height和width参数发挥作用
        self.display_frame.pack_propagate(0)
        self.display_frame.pack(fill=BOTH, side=TOP, expand=True)
        self.control_frame.pack_propagate(0)
        self.control_frame.pack(fill=BOTH, side=BOTTOM, expand=True)

        self.graph_frame.pack_propagate(0)
        self.graph_frame.pack(fill=BOTH, side=LEFT, expand=True)
        self.infor_frame.pack_propagate(0)
        self.infor_frame.pack(fill=BOTH, side=RIGHT, expand=True)

        self.register_frame.pack_propagate(0)
        self.register_frame.pack(fill=BOTH, side=LEFT, expand=True)
        self.conn_frame.pack_propagate(0)
        self.conn_frame.pack(fill=BOTH, side=RIGHT, expand=True)
        self.site_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)


        zhoudaqian = PhotoImage(file="zhoudaqian210.gif")
        rphotolabel = Label(self.register_frame,
                            image=zhoudaqian,
                            justify=CENTER,
                            bg = "white"
                            )
        rphotolabel.place(relx=0.025, rely=0.05, relwidth=0.3, relheight=0.9)
        sqlbutton = Button(self.conn_frame, text="接数据库",
                           font=('华康少女字体', 20),
                           fg="black",
                           bg='steelblue',
                           command=self.connsql_button).place(relx=0.32, rely=0.3, relwidth=0.22, relheight=0.23)
        com = Uart(conn_frame=self.conn_frame)
        com.main_func()
        read_com = com.read_com()
        com_th = threading.Thread(target=read_com)
        com_th.setDaemon(True)
        com_th.start()
        com_th.join()
        # main_th = threading.Thread(target=main())
        # main_th.setDaemon(True)
        # main_th.start()
        # main_th.join()


    def connsql_button(self):
        sitenum = self.sitenumvar.get()
        connsql = ConnSql()
        sqlsite,site_N,site_W,_ = connsql.readdata(sitenum)   #获得所选数据库的信息：站点编号, N,W, gsm号码，
        print("sqlsite{},site_N{},site_W{}".format(sqlsite,site_N,site_W) )
        try:
            print("向infor写入信息")
            information = Infor( infor_frame=self.infor_frame, sqlsite=sqlsite, site_N=site_N, site_W=site_W, sqlpredict=47,
                                 site_frame=self.site_frame,)
            infor_main = information.main_func()
            #print("执行标记1")
            graph = Graph( graph_frame=self.graph_frame, sitenum=sqlsite )
            graph.main_func()
            #print("执行标记2")
            predictgraph = PredictGraph( infor_frame=self.infor_frame, sitenum=sqlsite )
            predictgraph.main_func()
            #print("执行标记3")

            print("连接数据库成功")
            messagebox.showinfo("连接数据库", "连接数据库成功")
        except:
            messagebox.showerror("连接数据库","连接数据库失败")
        finally:
            predictinfor = PredictInfor( sitenum=sqlsite, site_frame=self.site_frame )
            predictinfor.warning_infor()

class Login():
    def __init__(self):
        self.login_frame = Frame( root, height=800, width=1000 )
        self.root_username = 'root'
        self.root_password = 'root'

    def login(self):
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(fill=BOTH, side=LEFT, expand=True)
        self.titlelabel = Label(self.login_frame, text="森林卫士环境监测系统",
                              font=("华康少女字体", 40))
        self.titlelabel.place(relx=0.12, rely=0.03, relwidth=0.7, relheight=0.3)

        print("login_button函数执行2")
        self.username = StringVar()
        self.password = StringVar()
        self.usernamelabel = Label(self.login_frame, text="账号：",
                              font=("华康少女字体", 20))
        self.usernamelabel.place(relx=0.25, rely=0.33, relwidth=0.2, relheight=0.08)

        self.username_entry = Entry(self.login_frame)
        self.username_entry.place(relx=0.43, rely=0.33, relwidth=0.2, relheight=0.08)
        print("login_button函数执行3")
        self.passwordlabel = Label(self.login_frame, text="密码：",
                              font=("华康少女字体", 20))
        self.passwordlabel.place(relx=0.25, rely=0.45, relwidth=0.2, relheight=0.08)
        self.password_entry = Entry(self.login_frame)
        self.password_entry.place(relx=0.43, rely=0.45, relwidth=0.2, relheight=0.08)

        self.passwordbutton = Button(self.login_frame, text="密码登录",
                             font=("华康少女字体", 20),
                             fg="black",
                             bg='steelblue',
                             command=self.password_check)
        self.passwordbutton.place(relx=0.45, rely=0.58, relwidth=0.18, relheight=0.08)

        self.facebutton = Button(self.login_frame, text="人脸登录",
                             font=("华康少女字体", 20),
                             fg="black",
                             bg='steelblue',
                             command=self.faceid_check)
        self.facebutton.place(relx=0.25, rely=0.58, relwidth=0.18, relheight=0.08)


    def password_check(self):
        self.username_input = self.username_entry.get()
        self.password_input = self.password_entry.get()
        if self.username_input == self.root_username and self.password_input== self.root_password:
            self.login_frame.destroy()
            slws = SenlinWeiShi()
            slws.main()
            messagebox.showinfo("登录成功", "登录成功")
        else:
            messagebox.showerror("登录失败", "用户名或密码错误")

    def faceid_check(self):
        if face_rec():
            self.login_frame.destroy()
            slws = SenlinWeiShi()
            slws.main()
            messagebox.showinfo("登录成功", "登录成功")
if __name__ == "__main__":
    #传入infor参数

    login = Login()
    login.login()
    # print( "主函数进程%s"%main_th.is_alive() )
    # print( "串口函数进程%是" )
    mainloop()


