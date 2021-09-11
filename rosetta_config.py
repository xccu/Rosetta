import configparser
import os

#https://www.cnblogs.com/imyalost/p/8857896.html
class Config():
    def __init__(self,path='config.ini'):
        self.path=path
        self.cfg = configparser.ConfigParser()
        
    def get_sections(self):
        self.cfg.read(self.path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        return self.cfg.sections()

    def get_option(self,section,option):
        self.cfg.read(self.path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        return self.cfg.get(section, option) # 获取[Mysql-Database]中host对应的值
    
    def set_value(self,section,option,value):
        self.cfg.set(section, option,value)  # 获取[Mysql-Database]中host对应的值
        with open(self.path,"w+") as f:
            self.cfg.write(f) 
