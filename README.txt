开闸放水所对应的下拉列表需关联对应的站点at指令和gsm号码才能向对应的下位机站点发送指令，
现在只能向串口发送1

其余部分完整可打包程序

切换到slws文件所在目录下，使用下面命令进行打包，文件中包含zhoudaqian210图片
需要将图片放到dist目录下
pyinstaller --hidden-import tkinter.filedialog -F slws.py
无控制台（小黑窗）打包：pyinstaller --hidden-import tkinter.filedialog -F -w slws.py
程序中要把这句注释掉，不然会程序无响应
#            site_frame.after(1000, warning_infor )

因为软件中设置有绝对路径的原因，所以该目录要放在D盘下运行，且目录名不能更改