"""
Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)
"""

# -*- coding: utf-8 -*-
__author__ = 'Lin'

import codecs
import string


def test():
    "先测试一下一句话的词频分析法，参考上一题的数据"
    # 好吧，只有一行数据果然太少了，字典对应的61才是正确的，可是61只出现了1次
    # 这里采取的思路是，这里面肯定有一个对应着e，所以把每个都遍历一遍就是了
    # 判断是否为英文语句的标准是，空格的数量，嘿嘿~~
    hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    bytes_string = codecs.decode(hex_string, "hex")

    characters = []
    for value in set(bytes_string):
        character = chr(value ^ ord('e'))
        if character in string.ascii_letters:
            characters.append(character)

    for each_ch in characters:
        each_ch = codecs.encode(each_ch, "ascii") * len(bytes_string)
        decrypto_text = byte_xor(each_ch, bytes_string)
        if decrypto_text.count(b' ') > 3:
            print(decrypto_text)


def byte_xor(bytes1, bytes2):
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


def main():
    blocks = []
    with open("task4.txt", "r") as f:
        # block_size = 60 # 坑了，有一部分没有60字节，所以不能这样读
        data = f.readline().strip()
        while data != '':
            blocks.append(data)
            data = f.readline().strip()

    for each_block in blocks:
        each_block = codecs.decode(each_block, "hex")
        value_set = set(each_block)

        for value in value_set:
            character = hex(value ^ ord('e'))[2:].zfill(2)  # 之前错误的原因在于以为异或的只有英文字母
            character_string = codecs.decode(character, "hex") * len(each_block)
            decrypto_text = byte_xor(each_block, character_string)
            if decrypto_text.count(b' ') > 3:  # 3这个基准可以修改的
                print(decrypto_text)


if __name__ == '__main__':
    main()
    # test()

