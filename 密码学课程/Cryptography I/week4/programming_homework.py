# -*- coding: utf-8 -*-
__author__ = 'Lin'

import urllib.request  # urllib.request在python3.x中被改为urllib.request
import binascii
from itertools import zip_longest

# padding oracle attack
# 思路参考课件
# writeUp http://blog.csdn.net/csh1989/article/details/38457377
# writeUp http://www.cyberfez.com/class/tls-attack.html
# optimize:依据词频分析法来跑，而不是遍历256

target_url = 'http://crypto-class.appspot.com/po?er='
dictionary = "e taoinshrdlcumwfgypbvkjxqzETAOINSHRDLCUMWFGYPBVKJXQZ"


class PaddingOracle(object):
    def query(self, q):
        target = target_url + urllib.request.quote(q)  # Create query URL

        # 设置代理，要不然连不上
        # goagent : 127.0.0.1:8087 ; wujie: 127.0.0.1:9666
        proxy_support = urllib.request.ProxyHandler({"http": "127.0.0.1:8087"})
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0')]
        urllib.request.install_opener(opener)

        response = urllib.request.Request(target)  # Send HTTP request to server
        try:
            f = urllib.request.urlopen(response)  # Wait for response
            code = f.getcode()
            if code == 200:
                return code
        except urllib.request.HTTPError as e:
            # print("We got: %d" % e.code)  # Print response code
            print(".", end='', flush=True)  # 这里得加flush=True，要不然不打印
            if e.code == 404:
                return True  # good padding
            return False  # bad padding


def main():
    original_quote = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f" \
                     "748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0" \
                     "bdf302936266926ff37dbf7035d5eeb4"

    blocks = divide_group(original_quote, 32)

    plaintext = ""
    for i in range(len(blocks) - 1):
        plaintext += (get_plaintext(blocks[i], blocks[i + 1]))

    # 最后一个密文分组本身就有padding，需要特殊处理
    plaintext += (get_last_block_plaintext(blocks[-2], blocks[-1]))

    print(plaintext)


def get_plaintext(pre_ciphertext, ciphertext):
    """输入的pre_ciphertext和ciphretext都是32个十六进制数，str形式
    输出的是ascii编码，str形式"""

    intermediary_value = []
    po = PaddingOracle()
    pre_ciphertext = binascii.unhexlify(pre_ciphertext)
    plaintext = ""
    for order in range(16):
        guess_ciphertext = change_pre_ciphertext(order + 1, intermediary_value)
        for guess_value in dictionary:
            guess_ciphertext[-(order + 1)] = ord(guess_value) ^ pre_ciphertext[-(order + 1)] ^ (order + 1)
            quote = binascii.hexlify(guess_ciphertext).decode("utf-8") + ciphertext

            if po.query(quote) is True:
                intermediary_value.insert(0, ord(guess_value) ^ pre_ciphertext[-(order + 1)])
                plaintext = guess_value + plaintext
                print(quote)
                break

    return plaintext


def get_last_block_plaintext(pre_ciphertext, ciphertext):
    """输入的pre_ciphertext和ciphertext均为32位16进制数，str形式
       输出的plaintext为ascii编码，str形式
       通过最后一个字节明文padding值, 然后除了padding值以外的明文都按之前的方法猜解"""
    intermediary_value = []
    plaintext = ""
    po = PaddingOracle()
    pre_ciphertext = binascii.unhexlify(pre_ciphertext)
    guess_ciphertext = bytearray(16)

    for guess_value in range(1, 17):
        guess_ciphertext[-1] = guess_value ^ pre_ciphertext[-1] ^ 1
        quote = binascii.hexlify(guess_ciphertext).decode("utf-8") + ciphertext

        if po.query(quote) is True:
            padding_value = guess_value
            print("padding_value = {0}".format(padding_value))
            break

    # 这一部分明显重复了，有待优化啊
    for order in range(padding_value):
        intermediary_value.insert(0, padding_value ^ pre_ciphertext[-(order + 1)])

    for order in range(padding_value, 16):
        guess_ciphertext = change_pre_ciphertext(order + 1, intermediary_value)
        for guess_value in dictionary:
            guess_ciphertext[-(order + 1)] = ord(guess_value) ^ pre_ciphertext[-(order + 1)] ^ (order + 1)
            quote = binascii.hexlify(guess_ciphertext).decode("utf-8") + ciphertext

            if po.query(quote) is True:
                intermediary_value.insert(0, ord(guess_value) ^ pre_ciphertext[-(order + 1)])
                plaintext = guess_value + plaintext
                print(quote)
                break

    return plaintext


def change_pre_ciphertext(order, intermediary_value):
    """
    输入的参数order为int型
    intermediary_value为列表，每个元素均为十进制表示
    输出为bytearray型
    """
    result = bytearray(16)
    for index in range(order - 1):
        result[-(index + 1)] = intermediary_value[-(index + 1)] ^ order

    return result


def divide_group(iterable, n):
    """Collect data into fixed-length chunks or blocks"""
    # grouper("ABCDEFG", 3, 'x') --> (A, B, C), (D, E, F), (G, x, x)"
    args = [iter(iterable)] * n

    blocks = []
    for block in zip_longest(*args):
        blocks.append("".join(block))

    return blocks


if __name__ == "__main__":
    main()