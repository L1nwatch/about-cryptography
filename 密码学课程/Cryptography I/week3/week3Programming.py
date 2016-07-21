# -*- coding: utf-8 -*-
__author__ = 'Lin'

# 被坑爹的SHA256.update()这个方法害了好久，详见test()

from Crypto.Hash import SHA256
import math
import codecs

target_file_name = "6 - 1 - Introduction (11 min).mp4"

test_file_name = "6 - 2 - Generic birthday attack (16 min).mp4"
test_file_hash = "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"


def main():
    blocks = []
    block_size = 1024

    # 参考了答案了思路，比直接一口气读完全部好得多，原因是一口气读完还得处理非整数倍的块
    with codecs.open(target_file_name, 'rb') as f:
        data = f.read(block_size)
        while data != b'':
            blocks.insert(0, data)  # 省得转置了
            data = f.read(block_size)

    h = b''
    for each_block in blocks:  # 参考了writeUp的写法，这样省去专门处理第一个块的语句了
        h = SHA256.new(each_block + h).digest()

    print(codecs.encode(h, "hex"))


def test():
    "坑爹的SHA256.update()，结果发现第二次异或结果就开始不一样了"
    text = b'aa'
    new_text = b'cc'

    hash = SHA256.new()
    hash.update(text)
    print("first hash:{0}".format(hash.digest()))
    hash.update(new_text)
    print("Second hash:{0}".format(hash.digest()))

    print("first hash:{0}".format(SHA256.new(text).digest()))
    print("Second hash:{0}".format(SHA256.new(new_text).digest()))


if __name__ == '__main__':
    main()

