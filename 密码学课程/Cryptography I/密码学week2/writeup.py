# 以下为python2.X版本的题解
'''
import sys
from Crypto.Cipher import AES
from Crypto import Random
BLOCKSIZE=16
def strxor(a, b):
    """ xor two strings of different lengths """
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def encry_CBC_AES(key,message):
    """ AES encryption in CBC mode """
    pad=BLOCKSIZE-len(message)%BLOCKSIZE #padding
    for dummy_idx in range(pad):
        m=m+chr(pad)

    cipher = AES.new(key, AES.MODE_ECB)
    iv = Random.new().read(BLOCKSIZE)
    result=iv
    for idx in range(len(message)/BLOCKSIZE):
        ciphertext=cipher.encrypt(strxor(message[idx*BLOCKSIZE:(idx+1)*BLOCKSIZE],iv))
        iv=ciphertext
        result+=ciphertext
    return result

def decry_CBC_AES(key,ciphertext):
    """ AES decryption in CBC mode """
    cipher = AES.new(key, AES.MODE_ECB)
    iv = ciphertext[:BLOCKSIZE]
    result=''
    for idx in range(1,len(ciphertext)/BLOCKSIZE):
        message=strxor(cipher.decrypt(ciphertext[idx*BLOCKSIZE:(idx+1)*BLOCKSIZE]),iv)
        iv=ciphertext[idx*BLOCKSIZE:(idx+1)*BLOCKSIZE]
        result+=message
    pad=len(result)
    return result[:pad-ord(result[pad-1])] # abandon the padding

key='140b41b22a29beb4061bda66b6747e14'.decode('hex')
msg1='4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'.decode('hex')
msg2='5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'.decode('hex')
print decry_CBC_AES(key,msg1)
print decry_CBC_AES(key,msg2)
'''