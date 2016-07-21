# -*- coding: utf-8 -*-
__author__ = 'Lin'

# 以下写的是python3, 参考笔记里给的AES代码
# 一开始思路错了，以为直接用AES解密就能出结果，但其实不是！看一下笔记，还需要异或的！
# 思路看一下Week2Homework的Question8解析
# 注意AES的分块是16bytes也就是128bits！密钥也是128bits不是128bytes
# 注意需要先用codecs.decode编码成二进制，不能直接加个b''就完事了



import codecs
from Crypto.Cipher import AES
from Crypto.Util import Counter
import math


def main():
    cbc_key = "140b41b22a29beb4061bda66b6747e14"
    cbc_ciphertexts = [
        "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81",
        "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    ]

    ctr_key = "36f18357be4dbd77f050515c73fcf9f2"
    ctr_ciphertexts = [
        "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329",
        "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
    ]

    cbc_decrypt(cbc_ciphertexts, cbc_key)
    ctr_decrypt(ctr_ciphertexts, ctr_key)


def cbc_decrypt(cbc_ciphertexts, cbc_key):
    "这里演示了两种方法，一种是用ECB自己手动实现CBC，另一种直接就用库里自带的CBC"
    block_size = 16
    print("CBC:")
    key = codecs.decode(cbc_key, "hex")
    for ciphertext in cbc_ciphertexts:
        ciphertext = codecs.decode(ciphertext, "hex")

        # 这里用基本的ECB模式, 然后自己实现了CBC模式
        iv = ciphertext[:block_size]
        plaintext = b""
        cipher = AES.new(key, AES.MODE_ECB)
        for index in range(1, math.ceil(len(ciphertext) / block_size)):  # 这里注意不用//除法
            tmp = cipher.decrypt(ciphertext[index * block_size:(index + 1) * block_size])
            plaintext += bytes_xor(tmp, iv)
            iv = ciphertext[index * block_size:(index + 1) * block_size]

        pad = plaintext[-1]  # pad的数字即字节数，比如说\x01, \x02\x02之类的
        print(plaintext[:len(plaintext) - pad])

        # 内置的AES实现的CBC模式
        iv = ciphertext[:block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = ciphertext[block_size:]
        plaintext = cipher.decrypt(ciphertext)
        plaintext = plaintext[:len(plaintext) - plaintext[-1]]
        print(plaintext)


def ctr_decrypt(ctr_ciphertexts, ctr_key):
    block_size = 16
    ctr_key = codecs.decode(ctr_key, "hex")

    # 以下利用基本的AES_ECB模式 + 自己手动实现CTR
    for ciphertext in ctr_ciphertexts:
        int_iv = int(ciphertext[:block_size * 2], 16)  # 这里注意得乘2，要不然取少了一半
        ciphertext = codecs.decode(ciphertext, "hex")
        decryptor = AES.new(ctr_key, AES.MODE_ECB)

        plaintext = b""
        for index in range(1, math.ceil(len(ciphertext) / block_size)):  # 这里注意不用//除法
            iv = codecs.decode(hex(int_iv)[2:], "hex")

            tmp = decryptor.encrypt(iv)  # 注意这里用到的并不是decrypt
            plaintext_part = bytes_xor(tmp, ciphertext[index * block_size:(index + 1) * block_size])
            plaintext += plaintext_part

            int_iv += 1

        print(plaintext)

    # 以下利用内置的AES_CTR解决
    for ciphertext in ctr_ciphertexts:
        iv = int(ciphertext[:block_size * 2], 16)
        # Counter的使用说明
        # https://www.dlitz.net/software/pycrypto/api/current/Crypto.Util.Counter-module.html
        counter = Counter.new(128, initial_value=iv)
        ciphertext = codecs.decode(ciphertext, "hex")[block_size:]
        decryptor = AES.new(ctr_key, AES.MODE_CTR, counter=counter)

        print(decryptor.decrypt(ciphertext))


def bytes_xor(bytes1, bytes2):
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


if __name__ == '__main__':
    main()
