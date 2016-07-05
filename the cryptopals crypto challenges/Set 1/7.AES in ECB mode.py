"""
AES in ECB mode

The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".

(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
Do this with code.

You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. You'll need it a lot later on, and not just for attacking ECB.
===================================================================================================================================================
【回头最好再用OpenSSL再实现一次】

"""
# -*- coding: utf-8 -*-
__author__ = 'Lin'

# url: http://cryptopals.com/sets/1/challenges/7/
# 题意: 给了AES密钥, 给了密文文件, 解密一下就行
# 题目提示说用OpenSSL，但是我这里用的PyCrypto
from Crypto.Cipher import AES
import base64


def main():
    file_name = "task7.txt"
    key = "YELLOW SUBMARINE"
    file_content = get_file_content(file_name)

    data = b''
    for each_block in file_content:
        data += base64.b64decode(each_block)

    decryptor = AES.new(key, AES.MODE_ECB)
    print(decryptor.decrypt(data))


def get_file_content(file_name, block_size=16):
    """
    按块读取文件内容（为了AES解密需要）, 题目已经说了是128bits，所以按16字节分组
    :param file_name: "task7.txt"
    :param block_size: 128
    :return: [b'a', b'b', b'c', ...]
    """
    blocks = []
    with open(file_name, 'r') as f:
        data = f.read(block_size)
        while data != '':
            blocks.append(data)
            data = f.read(block_size)

    return blocks


if __name__ == '__main__':
    main()


