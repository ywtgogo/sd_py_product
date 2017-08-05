#_*_ coding:utf-8 _*_

import requests
#from test_lib import *
import os,time,datetime
from sys  import *
import base64
from Crypto.Cipher import AES

import json



def nrPadBytes(blocksize, size):
    'Return number of required pad bytes for block of size.'
    if not (0 < blocksize < 255):
        print "blocksize must be between 0 and 255!!!!!!!!!!!!!!!!!!!!!!!!!!"
    return blocksize - (size % blocksize)


def appendPadding(blocksize, s):
    '''Append rfc 1423 padding to string.
    RFC 1423 algorithm adds 1 up to blocksize padding bytes to string s. Each
    padding byte contains the number of padding bytes.
    '''
    n = nrPadBytes(blocksize, len(s))
    if n==0:
        return s + (chr(16) * 16)
    else:
        return s + (chr(n) * n)


def removePadding(blocksize, s):
    'Remove rfc 1423 padding from string.'
    n = ord(s[-1])  # last byte contains number of padding bytes
    if n > blocksize or n > len(s):
        print('invalid padding!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return s[:-n]




def encryptAes(key, string):
    mode = AES.MODE_CBC
    #IV = appendPadding(16, 'AES')
    IV = 'SandlacusData#@1'
    encryptor = AES.new(key, mode, IV)
    str_pad = appendPadding(16, string)
    #print "len of str_pad: %d" %len(str_pad)
    result = encryptor.encrypt(str_pad)
    return result


def decryptAes(key, string):
    mode = AES.MODE_CBC
    #IV = appendPadding(16, 'AES')
    IV = 'SandlacusData#@1'
    decryptor = AES.new(key, mode,IV)
    result = decryptor.decrypt(string)
    str_rmpad = removePadding(16, result)
    return str_rmpad


