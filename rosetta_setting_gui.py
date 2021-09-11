from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Setting_Window():

    #构造函数
    def __init__(self,window):
        self.window = window


    #初始化
    def init(self):
        #设置窗体title

        self.window.title('Setting')
        #设置窗体宽高
        self.window.geometry("400x300")
        
        self.container = Frame(self.window, width=400, height=300,background="#F2F2F2")
        self.container.pack()
