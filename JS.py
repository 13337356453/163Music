import base64
import random
from binascii import hexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class JS:
    @staticmethod
    def d(d,e="010001",f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7",g="0CoJUm6Qyw8W8jud"):
        '''生成数据'''
        i=JS.a(16)
        h_encText=JS.b(d,g)
        encText=JS.b(h_encText,i)
        encSecKey=JS.c(i,e,f)
        return encText,encSecKey
    @staticmethod
    def a(a):
        '''生成16位随机字符'''
        b="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        c=""
        for i in range(a):
            e = random.randint(0, len(b) - 1)
            c+=b[e]
        return c
    @staticmethod
    def b(a,b):
        '''AES加密'''
        key = b.encode('utf-8')
        iv = "0102030405060708".encode('utf-8')
        data = a.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')
    @staticmethod
    def c(a,b,c):
        '''RSA加密'''
        a = a[::-1]
        result = pow(int(hexlify(a.encode()), 16), int(b, 16), int(c, 16))
        return format(result, 'x').zfill(131)