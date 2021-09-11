from Crypto.Cipher import AES
import base64
import os
from rosetta_interface import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKC
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as Signature_PKC
import threading
import random
import string
from time import *
from rosetta_util import *

aes_key_path="keys/aes_key.pem"
rsa_public_path="keys/rsa_public.pem"
rsa_private_path="keys/rsa_private.pem"

#AES加密解密类
class AES_Encryptor(IEncryptor):
     #构造函数
    def __init__(self):
        self.file_Util = Flie_Util()
        self.exception_util=Exception_Util()
        self.progress=0
        #回调函数：进度
        self.progress_func=self.default_progress_func
        #回调函数：日志
        self.log_func = self.default_log_func

    #默认日志输出函数
    def default_log_func(self,progress):
        print(str(progress))
    
    #默认日志输出函数
    def default_progress_func(self,info):
        print(info)

    #生成密钥
    def create_key(self): 
        try:
            # 密钥key必须为 16（AES-128）， 24（AES-192）， 32（AES-256）
            # 32位随机字符串：密钥key+长度等于AES 块大小的不可重复的密钥向量
            key_list = [random.choice(string.digits + string.ascii_letters) for i in range(32)]
            key = ''.join(key_list).encode()
            with open(aes_key_path, "wb") as f:
                f.write(key)
            return "s_"
        except Exception as ex:
            return self.exception_util.print_exctption("create_key",ex)
        
    #加密
    def encrypt(self,filepath):
        temp = filepath[-4:]
        print(temp)
        #判断扩展名
        if filepath[-4:]=='.ros': 
            return "k_"
        try:
            #bytes读取文件
            bytes_array=self.file_Util.read_file_stream(filepath,2048)

            # 加载密钥和向量
            with open(aes_key_path, "rb") as f:
                key_str = f.read()
                key = key_str[0:16]
                iv = key_str[16:]

            # 使用 key 和iv 初始化AES 对象， 使用MODE_CFB模式
            self.mycipher = AES.new(key, AES.MODE_CFB, iv)

            # 分段加密
            en_bytes_array=[]
            i=0
            self.progress=0
            for bytes in bytes_array:
                i+=1
                self.setProgress(i,bytes_array)
                en_data = self.mycipher.encrypt(bytes)
                en_bytes_array.append(en_data)

            #写加密后的文件
            self.file_Util.write_file_stream(filepath,en_bytes_array)
            #重命名
            os.rename(filepath,filepath+'.ros')
            return "s_"
        except Exception as ex:
            return self.exception_util.print_exctption("encrypt",ex)

    #解密
    def decrypt(self,filepath):
        print(filepath[-4:])
        #判断扩展名
        if filepath[-4:]!='.ros': 
            return "k_"
        try:
            #bytes读取文件
            en_bytes_array=self.file_Util.read_file_stream(filepath,2048)

            # 加载密钥和向量
            with open(aes_key_path, "rb") as f:
                key_str = f.read()
                key = key_str[0:16]
                iv = key_str[16:]

            # 解密需要用key 和iv 生成的AES对象
            mydecrypt = AES.new(key, AES.MODE_CFB, iv)

            # 分段解密
            bytes_array=[]
            i=0
            self.progress=0
            for bytes in en_bytes_array:
                i+=1
                self.setProgress(i,en_bytes_array)
                data = mydecrypt.decrypt(bytes)
                bytes_array.append(data)
        
            #写解密后的文件
            self.file_Util.write_file_stream(filepath,bytes_array)
            #重命名
            os.rename(filepath,filepath[:-4])
            return "s_"
        except Exception as ex:
            return self.exception_util.get_exctption_info("decrypt",ex)
    
    #设置进度
    def setProgress(self,i,array):
        self.progress=(int)((i/len(array))*100)
        self.progress_func(self.progress)

#RSA加密解密类
class RSA_Encryptor(IEncryptor):
    
    #构造函数
    def __init__(self):
        self.file_Util = Flie_Util()
        self.exception_util=Exception_Util()
        self.encrypt_size=100
        self.decrypt_size=128
        #进度条进度
        self.progress=0
        #进度数值
        self.pro_num=0
        #文件大小
        self.file_size=0
        #字典数据
        self.dict_data={}
        #回调函数：进度
        self.progress_func=self.default_progress_func
        #回调函数：日志
        self.log_func = self.default_log_func

    #默认日志输出函数
    def default_log_func(self,progress):
        print(str(progress))
    
    #默认日志输出函数
    def default_progress_func(self,info):
        print(info)

    #创建RSA密钥对(公钥+私钥)
    def create_key(self):
        try:
            # 伪随机数生成器
            random_gen = Random.new().read
            # 生成秘钥对实例对象：1024是秘钥的长度
            rsa = RSA.generate(1024, random_gen)

            # 秘钥对的生成
            private_pem = rsa.exportKey()
            with open(rsa_private_path, "wb") as f:
                f.write(private_pem)

            public_pem = rsa.publickey().exportKey()
            with open(rsa_public_path, "wb") as f:
                f.write(public_pem)
            return "s_"
        except Exception as ex:
            return self.exception_util.print_exctption("create_rsa_key",ex)

    # 使用公钥对文件进行rsa 分段加密
    def encrypt(self,filepath):
        #判断扩展名
        if filepath[-4:]=='.ros': 
            return "k_"
        try:
            begin_time = time()

            self.file_size = os.path.getsize(filepath)  
            #bytes读取文件
            bytes_array=self.file_Util.read_file_stream(filepath,self.encrypt_size)      

            #if self.file_size > 10485760: #文件大于10M
            if True:
                en_bytes_array = self.get_encrypt_bytes_thread(bytes_array)
            else:
                en_bytes_array = self.get_encrypt_bytes(bytes_array)
        
            print(len(en_bytes_array))
            #写解密后的文件
            self.file_Util.write_file_stream(filepath,en_bytes_array)
            #重命名
            os.rename(filepath,filepath+'.ros')

            end_time = time()
            self.log_func('耗时：{}'.format(end_time-begin_time)) 

            return "s_"
        except Exception as ex:
             return self.exception_util.get_exctption_info("encrypt",ex)

    #获取加密后的字节数组
    def get_encrypt_bytes(self,bytes_array):
  
        self.log_func('单线程')

        # 加载公钥
        public_key = RSA.import_key(open(rsa_public_path).read() )
        
        # 分段加密
        en_bytes_array=[]
        cipher_rsa = Cipher_PKC.new(public_key)
        i=0
        self.progress=0
        for bytes in bytes_array:
            i+=1
            self.setProgress(i,bytes_array)
            en_data = cipher_rsa.encrypt(bytes)
            en_bytes_array.append(en_data)

        return en_bytes_array

    #获取加密后的字节数组（多线程）
    def get_encrypt_bytes_thread(self,bytes_array):
        
        self.log_func('多线程')

        # 加载公钥
        public_key = RSA.import_key(open(rsa_public_path).read() )

        self.pro_num=0
        self.progress=0
        self.dict_data.clear()

        self.log_func(len(bytes_array))
        thread_size = int(len(bytes_array)/10) #20个线程，单个线程解密大小
        # 创建线程列表
        threads = []
        # 分段解密
        cipher_rsa = Cipher_PKC.new(public_key)
        id = 0
        for i in range(0,len(bytes_array),thread_size): #每1M启动一个新线程
            t = threading.Thread(target=self.operate_thread, args=[id,bytes_array[i:i+thread_size],cipher_rsa.encrypt])
            t.start()
            threads.append(t)
            id += 1
        
        for t in threads:
            t.join()
        self.log_func("所有线程任务完成")

        # 按照字典的key排序输出
        en_bytes_array=[]
        for i in sorted (self.dict_data) : 
            #print('{}:{}'.format(i,len(self.dict_data[i])))
            j=0
            while j < len(self.dict_data[i]) :
                en_bytes_array.append(self.dict_data[i][j])
                j+=1

        return en_bytes_array
        

    # 使用私钥对文件进行rsa 分段解密
    def decrypt(self,filepath):     
        #判断扩展名
        if filepath[-4:]!='.ros': 
            return "k_"
        try:
            begin_time = time()

            self.file_size = os.path.getsize(filepath)  
            #bytes读取文件
            en_bytes_array=self.file_Util.read_file_stream(filepath,self.decrypt_size)      

            #if self.file_size > 10485760: #文件大于10M
            if True:
                bytes_array = self.get_decrypt_bytes_thread(en_bytes_array)
            else:
                bytes_array = self.get_decrypt_bytes(en_bytes_array)
        
            #写解密后的文件
            self.file_Util.write_file_stream(filepath,bytes_array)
            #重命名
            os.rename(filepath,filepath[:-4])

            end_time = time()
            self.log_func('耗时：{}'.format(end_time-begin_time)) 
            return "s_"
        except Exception as ex:
            return self.exception_util.get_exctption_info("encrypt",ex)

    #获取解密后的字节数组
    def get_decrypt_bytes(self,en_bytes_array):
  
        self.log_func('单线程')

        # 读取私钥
        private_key = RSA.import_key(open(rsa_private_path).read())

        # 分段解密
        bytes_array=[]
        cipher_rsa = Cipher_PKC.new(private_key)
        i=0
        self.progress=0
        for bytes in en_bytes_array:
            i+=1
            self.setProgress(i,en_bytes_array,self.decrypt_size)
            data = cipher_rsa.decrypt(bytes,None)
            bytes_array.append(data)

        return bytes_array

    #获取解密后的字节数组（多线程）
    def get_decrypt_bytes_thread(self,en_bytes_array):
        
        self.log_func('多线程')

        # 读取私钥
        private_key = RSA.import_key(open(rsa_private_path).read())

        self.pro_num=0
        self.progress=0
        self.dict_data.clear()

        self.log_func(len(en_bytes_array))
        thread_size = int(len(en_bytes_array)/5) #20个线程，单个线程解密大小
        # 创建线程列表
        threads = []
        # 分段解密
        cipher_rsa = Cipher_PKC.new(private_key)
        id = 0
        for i in range(0,len(en_bytes_array),thread_size): #每1M启动一个新线程
            t = threading.Thread(target=self.operate_thread, args=[id,en_bytes_array[i:i+thread_size],cipher_rsa.decrypt])
            t.start()
            threads.append(t)
            id += 1
        
        for t in threads:
            t.join()
        self.log_func("所有线程任务完成")

        # 按照字典的key排序输出
        bytes_array=[]
        for i in sorted (self.dict_data) : 
            #print('{}:{}'.format(i,len(self.dict_data[i])))
            j=0
            while j < len(self.dict_data[i]) :
                bytes_array.append(self.dict_data[i][j])
                j+=1

        return bytes_array

    #多线程加密/解密操作
    def operate_thread(self,id,array,rsa):
        self.log_func('线程{} 大小{}'.format(id,len(array)))
        method_name = rsa.__name__
        datas =[]
        for bytes in array:
            self.pro_num+=1
            if method_name=='decrypt':    #解密
                self.setProgress(self.pro_num,array,self.decrypt_size)
                datas.append(rsa(bytes,None))
            elif method_name=='encrypt':  #加密
                self.setProgress(self.pro_num,array,self.encrypt_size)
                datas.append(rsa(bytes))
        self.dict_data[id] = datas
            
    #设置进度
    def setProgress(self,i,array,single_size = 100):
        self.progress=(int)((i/(self.file_size/single_size))*100)
        #print("({}/{})*100={}".format(i,self.file_size/single_size,self.progress))
        self.progress_func(self.progress)

