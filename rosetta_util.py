import base64
import os



#文件读写类
class Flie_Util():
    #构造函数
    def __init__(self):
        self.exception_util=Exception_Util()
        self.s=""

    #读文件
    def read(self,filePath):
        try:
            f = open(filePath, 'r')
            result = f.read()
            return result
        except Exception as ex:
            return self.exception_util.get_exctption_info("read",ex)
        finally:
            if f:
                f.close()
    
    #写文件
    def write(self,filePath,data):
        try:
            f = open(filePath, 'w')
            f.write(data)
            f.write(bytes)
        except Exception as ex:
             self.exception_util.print_exctption("write",ex)
        finally:
            if f:
                f.close()

    #写字节
    def write_bytes(self,filePath,bytes):
        try:
            f = open(filePath, 'wb')
            f.write(bytes)
        except Exception as ex:
             self.exception_util.print_exctption("write_bytes",ex)
        finally:
            if f:
                f.close()

    #bytes分段读取文件
    def read_file_stream(self,filepath,length):
        bytes_array=[]
        try:
            f = open(filepath,'rb')
            while True:
                dt=f.read(length)
                if dt is not b'': #读取到结尾则结束
                    bytes_array.append(dt)
                    #print(dt)
                else:
                    break
        except Exception as ex:
             self.exception_util.print_exctption("read_file_stream",ex)
        finally:
            if f:
                f.close()
        return bytes_array

    #bytes列表写入文件
    def write_file_stream(self,filepath,bytes_array):
        try:
            f= open(filepath, 'wb')
            f.writelines(bytes_array)
        except Exception as ex:
             self.exception_util.print_exctption("write_file_stream",ex)
        finally:
            if f:
                f.close()
    
    #遍历指定文件夹中所有文件
    def foreach_folder(self,path):
        filelist=[]
        for root,dirs,files in os.walk(path):
            for name in files:
                path = os.path.join(root,name)
                filelist.append(path)
                print(path)
        return filelist
    
    def judge_path(self,path):
        if os.path.isdir(path):     #文件夹返回0
            print("文件夹"+path)
            return 0
        elif os.path.isfile(path):  #文件返回1
            print("文件"+path)
            return 1
        else:
            print("未识别"+path)
            return -1
 

class Exception_Util():
     #构造函数
    def __init__(self):
        self.s=""

    def print_exctption(self, msg,e):
        errorstr=self.get_exctption_info(msg,e)
        print(errorstr)

    def get_exctption_info(self,exStr, e):
        s='error:\t'
        s+=(exStr)
        s+=('\nstr(e):\t')
        s+=(str(e))
        s+=('\nrepr(e):\t')
        s+=(repr(e))
        return s