
#https://blog.csdn.net/yangxiaodong88/article/details/80801278

from Crypto.Cipher import AES
from Crypto import Random

# 要加密的明文
data = 'En Taro Tallnut'
# 密钥key必须为 16（AES-128）， 24（AES-192）， 32（AES-256）
key = b'this is a 16 key'
# 生成长度等于AES 块大小的不可重复的密钥向量
iv = Random.new().read(AES.block_size)
print("密钥:{}".format(iv))
# 使用 key 和iv 初始化AES 对象， 使用MODE_CFB模式
mycipher = AES.new(key, AES.MODE_CFB, iv)
print(mycipher)

# 加密的明文长度必须为16的倍数， 如果长度不为16的倍数， 则需要补足为16的倍数
# 将iv(密钥向量)加到加密的密钥开头， 一起传输
ciptext = iv + mycipher.encrypt(data.encode())

# 解密的话需要用key 和iv 生成的AES对象
print("密文:{}".format(ciptext))
mydecrypt = AES.new(key, AES.MODE_CFB, ciptext[:16])
# 使用新生成的AES 对象， 将加密的密钥解密
decrytext = mydecrypt.decrypt(ciptext[16:])
print(decrytext.decode())