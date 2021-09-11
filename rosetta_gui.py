from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from rosetta_config import *
from rosetta_encryptor import *
from rosetta_util import *
from rosetta_gui_expand import *
from rosetta_setting_gui import *
import _thread
import time


class Init_Window():
    
    #构造函数
    def __init__(self,window):
        self.window = window
        self.flag = False
        #self.window.overrideredirect(True);
        self.config = Config()
        encrypt_str="{0}_Encryptor".format( self.config.get_option("Encrypt","type"))
        print(encrypt_str) 
        #通过类名反射获取encryptor
        self.encryptor = globals()[encrypt_str]()
        self.file_util= Flie_Util()
        self.enable=True

    #初始化
    def init(self):
        #设置窗体title
        #𓂋𓍯𓋴𓇋𓏏𓏏𓄿
        self.window.title('Rosetta')
        #设置窗体宽高
        self.window.geometry("800x450")
        #self.window.grid(width=80, height=50)

        #固定宽高，防止用户调整尺寸
        self.window.resizable(0,0) 

        #self.window.toolbar = Frame(self.window, borderwidth=0)
        self.container = Frame(self.window, width=800, height=430,background="#F2F2F2")
        self.container.pack()

        self.head_frame = Frame(self.container, width=800, height=30,background="#4D4D4D")
        self.head_frame.place(x=0,y=0)

        self.cmd_frame = Frame(self.container, width=385, height=70,background="#FFFFFF")
        self.cmd_frame.place(x=10,y=40)

        self.setting_frame = Frame(self.container, width=385, height=70,background="#FFFFFF")
        self.setting_frame.place(x=405,y=40)

        #创建标签Label:默认的width, heigth表示字符个数和行数
        #文本内容：copyright by Charlie(圣书体)
        ft=("Arial", 30, "bold",)
        self.init_Label = Label_PX(self.head_frame,text="𓋴𓍯𓊪𓇌𓂋𓏭𓎼𓉔𓏏𓃀𓇌𓋴𓉔𓄿𓂋𓃭𓏭𓇋",width=360,height=30,bg="#4D4D4D",font = ft,fg = "white")
        self.init_Label.place(x=450,y=-1)

        #样式字典
        btn_styles = {
            'width':80,'height':23,'bd': 0,
            'background': "#00ABFF","enterBg":"#4D4D4D","fg":"white" ,
            "leaveBg":"#00ABFF","activebackground":"#7689ED",
            "compound":"left",'relief': "solid"
        }
        btn_out_styles = {'relief': "solid",'bd': 0,'bdcolor':"#BCBCBC","background":"#00ABFF","enterBg":"#4D4D4D","fg":"white","leaveBg":"#00ABFF","activebackground":"#7689ED",}
        text_styles = {'bd':1,'bdcolor':"#BCBCBC"}

        #加密按钮
        #self.encrypt_button = Button(self.container, text="加密", width=10,command=self.encrypt_click)  # 调用内部方法  加()为直接调用
        self.encrypt_button = Button_PX(self.cmd_frame, text="加密", image="img/encrypt.png", **btn_styles,command=self.encrypt_click)
        self.encrypt_button.place(x=10,y=10)

        #解密按钮
        self.decrypt_button = Button_PX(self.cmd_frame, text="解密", image="img/decrypt.png", **btn_styles,command=self.decrypt_click) 
        self.decrypt_button.place(x=10,y=35)

        #导出密钥按钮
        self.export_key_button = Button_PX(self.cmd_frame, text="导出密钥", **btn_styles)  
        self.export_key_button.place(x=100,y=10)

        #清空日志按钮
        self.clear_log_button = Button_PX(self.cmd_frame, text="清空日志",**btn_styles,command=self.clear_log_click)  
        self.clear_log_button.place(x=100,y=35)

        #生成密钥按钮
        self.create_key_button = Button_PX(self.cmd_frame, text="生成密钥",image="img/create-key.png", **btn_styles,command=self.create_keys_click) 
        self.create_key_button.place(x=190,y=10)

        #设置按钮
        self.setting_button = Button_PX(self.cmd_frame, text="设置", **btn_styles,command = self.setting_click) 
        self.setting_button.place(x=190,y=35)

        #测试按钮
        self.setting_button = Button_PX(self.cmd_frame, text="测试", **btn_styles,command=self.test) 
        self.setting_button.place(x=280,y=10)

        #选择文件按钮
        self.open_file_button = Button_PX(self.container, text="选择文件", width=80,**btn_out_styles,command=self.open_file_click) 
        self.open_file_button.place(x=10,y=130)

        #选择文件夹按钮
        self.open_folder_button = Button_PX(self.container, text="选择文件夹", width=80,**btn_out_styles,command=self.open_folder_click) 
        self.open_folder_button.place(x=100,y=130)

        #创建路径文本框
        self.file_Text = Text_PX(self.container, width=600, height=25,**text_styles)
        self.file_Text.place(x=190,y=130)

        #创建日志文本框
        #self.log_Text = Text(self.container, width=111, height=15)
        self.log_Text = Text_PX(self.container, width=780, height=200,**text_styles)
        self.log_Text.place(x=10,y=180)

        #创建进度条
        self.p_bar = ttk.Progressbar(self.container, length = 780, value = 0, mode = "determinate")
        self.p_bar.place(x=10,y=390)

        #底部状态栏:信息 
        self.status_bar = Label(self.window, text="就绪", bd=1, relief=SUNKEN,anchor=W,width=100)
        self.status_bar.pack(side=LEFT)

        #底部状态栏:计数 
        self.status_count_bar = Label(self.window, text="", bd=1, relief=SUNKEN,anchor=W)
        self.status_count_bar.pack(side=BOTTOM, fill=X)

        #设置进度条回调函数
        self.encryptor.progress_func=self.progress_callback
    
    #加密按钮响应函数
    def encrypt_click(self):
        if self.enable:
            result=self.file_util.judge_path(self.filePath)
            if result==0:
                _thread.start_new_thread(self.encrypt_folder_thread,())
            elif result==1:
                print("加密文件")
                _thread.start_new_thread(self.encrypt_thread,())
            else :
                self.log_Text.insert(1.0,'未能识别文件或文件夹\n')
        else:
            self.log_Text.insert(1.0,'加密程序正在运行中\n')

    #解密按钮响应函数
    def decrypt_click(self):
        if self.enable:
            result=self.file_util.judge_path(self.filePath)
            if result==0:
                _thread.start_new_thread(self.decrypt_folder_thread,())
            elif result==1:
                _thread.start_new_thread(self.decrypt_thread,())
            else :
                self.log_Text.insert(1.0,'未能识别文件或文件夹\n')
        else:
            self.log_Text.insert(1.0,'解密程序正在运行中\n')
            
    #文件加密线程函数
    def encrypt_thread(self):
        self.enable=False
        self.status_bar["text"] = '加密中：{0}'.format(self.filePath)
        self.status_count_bar["text"] = '1/1'
        self.encrypt(self.filePath)
        self.reset_control()
    
    #文件夹加密线程函数
    def encrypt_folder_thread(self):
        self.enable=False
        flie_list=self.file_util.foreach_folder(self.filePath)
        i=0
        count = len(flie_list)
        for file_name in flie_list:
            i+=1
            self.status_bar["text"] = '加密中：{0}'.format(file_name)
            self.status_count_bar["text"] = '{0}/{1}'.format(i,count)
            self.encrypt(file_name)
        self.log_Text.insert(1.0,'已加密：'+self.filePath+'\n')
        self.reset_control()

    #加密
    def encrypt(self,filePath):
        result = self.encryptor.encrypt(filePath)
        if result=="s_":
            self.log_Text.insert(1.0,'已加密：'+filePath+'\n')
        elif result=="k_":
            self.log_Text.insert(1.0,'已跳过：'+filePath+'\n')
        else:
            self.log_Text.insert(1.0,result+'\n')

    #文件解密线程函数
    def decrypt_thread(self):
        self.enable=False
        self.status_bar["text"] = '解密中：{0}'.format(self.filePath)
        self.status_count_bar["text"] = '1/1'
        self.decrypt(self.filePath)
        self.reset_control()
    
    #文件夹解密线程函数
    def decrypt_folder_thread(self):
        self.enable=False
        flie_list=self.file_util.foreach_folder(self.filePath)
        i=0
        count = len(flie_list)
        for file_name in flie_list:
            i+=1
            self.status_bar["text"] = '解密中：{0}'.format(file_name)
            self.status_count_bar["text"] = '{0}/{1}'.format(i,count)
            self.decrypt(file_name)
        self.log_Text.insert(1.0,'已解密：'+self.filePath+'\n')
        self.reset_control()

    #解密
    def decrypt(self,filePath):
        result = self.encryptor.decrypt(filePath)
        if result=="s_":
            self.log_Text.insert(1.0,'已解密：'+filePath+'\n')
        elif result=="k_":
            self.log_Text.insert(1.0,'已跳过：'+filePath+'\n')
        else:
            self.log_Text.insert(1.0,result+'\n')
    
    #打开文件函数
    def open_file_click(self):
        #self.window.withdraw()
        # 清空文本控件
        self.file_Text.delete('1.0','end')
        # 选择文件
        self.filePath = filedialog.askopenfilename()
        # 显示文件路径
        self.file_Text.insert(1.0,self.filePath)

    #打开文件夹函数
    def open_folder_click(self):
        # 清空文本控件
        self.file_Text.delete('1.0','end')
        # 选择文件夹
        self.filePath = filedialog.askdirectory()
        # 显示文件夹路径
        self.file_Text.insert(1.0,self.filePath)

    #生成密钥函数
    def create_keys_click(self):
        self.encryptor.create_key()
        self.log_Text.insert(1.0,'已生成密钥'+'\n')

    #打开设置窗口函数
    def setting_click(self):
        
        self.sub_Window =Setting_Window(Toplevel())
        self.sub_Window.init()

    #清空日志函数
    def clear_log_click(self):
        self.log_Text.delete('1.0','end')

    #进度条回调函数
    def progress_callback(self,i):
        #print(i)
        self.p_bar["value"]=i

    #控件复位函数
    def reset_control(self):
        self.status_bar["text"] = '就绪'
        self.status_count_bar["text"] = ''
        self.p_bar["value"]=0
        self.encryptor.progress=0
        self.enable=True

    #测试函数
    def test(self):
        self.window.overrideredirect(self.flag)
        self.flag=not self.flag