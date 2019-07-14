from tkinter import *

class TopMenu(object):
    def __init__(self, frame):
        self._root = frame
    def main_func(self):
        self.menuone = Menu( self._root )
        self.filemenu = Menu( self.menuone, tearoff=False )
        self.filemenu.add_command( label="查看最近三十天的数据",command=self.read30data)
        self.menuone.add_cascade( label="文件", font=("华康少女字体",30),menu=self.filemenu )
        self._root.config( menu=self.menuone )
    def read30data(self):
        print('被调用')