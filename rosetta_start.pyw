#import Gui
#from tkinter import *
from rosetta_gui import *

def main():

    # 实例化出一个父窗口
    window = Tk()             
    ZMJ_PORTAL =Init_Window(window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.init()
    # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    window.mainloop()          

main()