"""
Detect AES in ECB mode

In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

====================================================================================================================
"""
# -*- coding: utf-8 -*-
__author__ = 'Lin'

# 找到了好像一段重复的b'\x08d\x9a\xf7\r\xc0oO\xd5\xd2\xd6\x9ctL\xd2\x83'这一段重复了4次
# 这题不用解密, 所以不需要知道key, 只要找出每一行的重复密文就行了

from collections import Counter
from itertools import zip_longest


def main():
    file_name = "task8.txt"
    block_size = 32
    lines = get_file_lines(file_name)
    repeat_ciphertext = get_repeat_ciphertext(lines, times=2, block_size=block_size)
    print(repeat_ciphertext)


def get_file_lines(file_name):
    """input = "target_file.txt"
       output = ["line1\n", "line2\n", "line3\n"]"""
    with open(file_name, 'rU') as f:
        lines = f.readlines()

    return lines


def get_repeat_ciphertext(lines, times=1, block_size=1):
    """input:  ["line1\n", "line2\n", "line2\n"] line are all hex encoded
       output: [("line2", 2), ("line1", 1)]"""
    output = []
    for each_line in (l.strip() for l in lines):
        blocks = divide_group(each_line, block_size)
        for each in Counter(blocks).most_common():
            if each[1] > times:
                output.append(each)
            else:
                break

    return output


def divide_group(data, block_size=1):
    """input: 'abcdefghijklmno', block_size=3
       output: ['abc', 'def', 'ghi', 'jkl', 'mno']"""
    if len(data) % block_size != 0:
        raise ValueError

    args = [iter(data)] * block_size

    blocks = []
    for block in zip_longest(*args):
        blocks.append("".join(block))

    return blocks


if __name__ == "__main__":
    main()


'''
==================================================================================================================
网上WriteUp
# -*- coding: utf-8 -*-
__author__ = 'Lin'

from collections import Counter

# writeUp这里有点问题，如果blocksize的话就不适用AES了，AES是16字节而不是8字节（16的话是16个十六进制数）

def main():
    blocksize = 16

    # 参数'rU'，可以避免unix和windowx下换行符表示不同的问题(\r\n, \n)
    with open('task8.txt', 'rU') as f:
        # Read all lines available on the input stream and return them as a list of lines
        lines = f.readlines()

    # 这种分组方式可以学习一下
    for line in (l.strip() for l in lines):
        # list(range(0, 16 * 5, 16)) = [0, 16, 32, 48 ...], end够范围才有索引test(0, 16 * 5 + 1)
        indexes = range(0, len(line), blocksize)

        d = []
        for (start, end) in zip(indexes, indexes[1:]):
            d.append(line[start:end])

        # Counter('abcdeabcdabcaba').most_common(3)
        # 3表示，列举出3个出现次数最多的元素。
        cn = Counter(d)
        for each in cn.most_common():
            if each[1] > 1:
                print(each)
            else:
                break
        """
        这里得改进一下，这里判断条件只判断的最大值＞1的那一行，然后就把一整行的结果输出出来了
        if cn.most_common()[0][1] > 1:
            print(cn)
        """

if __name__ == "__main__":
    main()


'''