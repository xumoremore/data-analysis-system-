from tkinter import *
from register.registersql import RegisterSql  #需要注意包中调用模块的格式
from tkinter import messagebox
#relx=0.01, rely=0.01, relwidth=0.3, relheight=0.23
WIDTH = 0.6
HEIGHT = 0.2
X = 0.35
Y = 0.13
Y_INSTANCE = 0.03

LABEL_WIDTH= 0.3
MENU_WIDTH=0.3
REGI_WIDTH= 0.3
CAN_WIDTH= 0.3

LABEL_HEIGHT = HEIGHT
MENU_HEIGHT= HEIGHT
REGI_HEIGHT= HEIGHT
CAN_HEIGHT = HEIGHT
LABEL_X = X + Y_INSTANCE + REGI_WIDTH
MENU_X= X + Y_INSTANCE + CAN_WIDTH
REGI_X= X
CAN_X = X
LABEL_Y = Y_INSTANCE + Y
MENU_Y = LABEL_Y + LABEL_HEIGHT + Y_INSTANCE
REGI_Y =  Y_INSTANCE + Y
CAN_Y = REGI_Y + REGI_HEIGHT + Y_INSTANCE

class Register(object):
    '''
    site_message = None
    phone_message = None
    N_message = None
    W_message = None
    '''

    def __init__(self, register_frame, graph_frame ):
        self._register_frame = register_frame
        self._site_message = None
        self._phone_message = None
        self._N_message = None
        self._W_message = None

    def main_func(self):
        '''
        #主函数
        布局案件并且建立按键触发命令
        布置entry组件并且获取撤销与entry组件里相关的内容
        :return: 
        '''
        #电机注册按钮弹出注册对话框进行站点相关信息注册
        regibutton = Button( self._register_frame, text="注册",
                             font = ("华康少女字体", 20),
                             fg = "black",
                             bg='steelblue',
                             command=self.register_button ).place(relx=REGI_X, rely=REGI_Y, relwidth=REGI_WIDTH, relheight=REGI_HEIGHT )

        sitelabel = Label( self._register_frame, text=" 撤销站点：",
                           bg='white',
                           font = ("华康少女字体", 18)).place(relx=LABEL_X, rely=LABEL_Y, relwidth=LABEL_WIDTH, relheight=LABEL_HEIGHT )

        cancbutton = Button( self._register_frame, text="撤销",
                             font = ("华康少女字体", 20),
                             fg = "black",
                             bg = 'steelblue',
                             command=self.cancel_button ).place(relx=CAN_X, rely=CAN_Y, relwidth=CAN_WIDTH, relheight=CAN_HEIGHT)



        #使用optionmenu下拉列表控件获取要撤销的站点
        regi_look_site = RegisterSql(('0', '0', '0', '0'))
        sitenum_list = regi_look_site.exist_site()     #sitenum_list为一个元祖，如：((1,), (2,), (3,), (5,))
        if sitenum_list == []:
            sitenum_list = ["数据库无站点信息"]
        self._sitenumvar = StringVar()
        self._sitenumvar.set("选择站点")
        sitenum_om = OptionMenu(self._register_frame, self._sitenumvar, *sitenum_list)
        sitenum_om.place( relx=MENU_X, rely=MENU_Y, relwidth=MENU_WIDTH, relheight=MENU_HEIGHT )

        #删除optionmenu控件中选中的站点数据库相关信息，



    def register_button(self):
        '''
        不需要使用register_frame进行布局
        创建注册窗口的顶级窗口，用来执行注册站点的信息录入
        返回值：
        site_message
        phone_message
        N_message
        W_message
        :return: 
        '''
        print("注册按钮按下")
        FONT_TOP = ("华康少女字体", 15)
        PADX = 5
        PADY = 5
        register_top = Toplevel()
        register_top.title("站点注册")
        sitelabel = Label( register_top, text="选择站点编号：",
                               font = FONT_TOP).grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W )
        self._site_entry = Entry( register_top )
        self._site_entry.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W )


        phonelabel = Label( register_top, text="GSM号码：",
                               font = FONT_TOP).grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W )
        self._phone_entry = Entry( register_top)
        self._phone_entry.grid(row=1, column=1, padx=PADX, pady=PADY, sticky=W )


        placelabel = Label( register_top, text="地点：",
                               font = FONT_TOP).grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W )
        self._N_entry = Entry( register_top)
        self._N_entry.grid(row=2, column=1, padx=PADX, pady=PADY, sticky=W )

        Nlabel = Label( register_top, text="N",
                        font=FONT_TOP).grid(row=2, column=2, padx=PADX, pady=PADY, sticky=W)

        self._W_entry = Entry(register_top)
        self._W_entry.grid(row=2, column=3, padx=PADX, pady=PADY, sticky=W)
        Wlabel = Label( register_top, text="W",
                        font=FONT_TOP).grid(row=2, column=4, padx=PADX, pady=PADY, sticky=W)
        Button( register_top, text="注册该站点",
                font = FONT_TOP,
                command=self.regisite_button).grid(row=3, columnspan=5, padx=PADX, pady=PADY,)   #在这里self.register_site加不加括号是有区别的


    def regisite_button(self):
        #xx.get()数据类型均为字符串
        self._site_message = self._site_entry.get()
        self._phone_message = self._phone_entry.get()
        self._N_message = self._N_entry.get()
        self._W_message = self._W_entry.get()
        print(type(self._site_entry.get()))

        message = (self._site_message, self._N_message, self._W_message, self._phone_message )
        self._register_site = RegisterSql(message)
        self._register_site.createtable()
        print(message)


    def cancel_button(self):
        # 在没调用的时候被调属性和使用的属性都需要加self._才能共用
        #不加的话在该方法中无法被解析
        #删除总表siteinfor中的相关站点信息，以及属于该站点的数据表信息
        drop_site = RegisterSql(('0', '0', '0', '0'))
        cancel_flat = messagebox.askokcancel("撤销站点", "是否要撤销该站点" )
        if cancel_flat:
            drop_table = drop_site.drop_table( sitenumvar = self._sitenumvar )
