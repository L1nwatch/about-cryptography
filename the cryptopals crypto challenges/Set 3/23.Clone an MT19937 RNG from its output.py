# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/3/challenges/23/
# 原题背景: MT19937后输入种子后, 每次调用extract_number()后都会输出新的值
# 如果我们得到由这个生成器产生的其中624个值, 我们就有办法得到跟这个MT19937同一个种子的随机数生成器
# 题意: 实现克隆MT19937
# 步骤：
# 1. 题目介绍说MT19937所使用到的temper是可逆的, 先要求我们写出其逆的算法
# 2. 利用步骤1得到的逆算法, 再利用得到的624个值, 我们就能够进行克隆工作
# 3. 验证是否克隆成功


# class MT19937是chall21的要求, 直接复制过来了(顺带自己美化了一下代码)
class MT19937:
    def __init__(self, seed):
        self.MT = [0] * 624
        self.index = 0
        self.seed = 0
        self.initialize_generator(seed)

    def initialize_generator(self, seed):
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = 0xffffffff & (0x6c078965 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i)

    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()

        y = self.MT[self.index]
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9d2c5680)
        y ^= ((y << 15) & 0xefc60000)
        y ^= (y >> 18)

        self.index = (self.index + 1) % 624
        return y

    def generate_numbers(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                self.MT[i] ^= 0x9908b0df


def main():
    # 测试自己写的逆算法是否为正确的
    test_untemper()

    raw_mt19937 = MT19937(6666)
    # 克隆工作
    clone_mt19937 = clone(raw_mt19937)

    # 测试克隆是否成功
    test_clone(raw_mt19937, clone_mt19937)
    print("Clone Success!")


def clone(mt):
    clone_mt = MT19937(0)
    # 利用步骤1得到的逆算法, 再利用624个值
    for i in range(624):
        clone_mt.MT[i] = untemper(mt.extract_number())

    return clone_mt


def test_clone(mt1, mt2):
    for i in range(10 ** 4):
        if mt1.extract_number() != mt2.extract_number():
            print("Clone Fail!")
            raise RuntimeError


def temper(y):
    # 这是MT19937里用到的算法, 参见MT19937类的extract_number()
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 0x9d2c5680)
    y = y ^ ((y << 15) & 0xefc60000)
    y = y ^ (y >> 18)

    return y


def untemper(y):
    # 以下算法参考网上资料https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html
    # 依次进行RightShiftXor、LeftShiftXorAnd、LeftShiftXorAnd、RightShiftXor

    y3 = (y & 0xffffc000)
    y3 |= ((y >> 18) ^ (y & 0x3fff))
    y2 = (y3 & 0x1039ffff)
    y2 |= ((y3 ^ ((y2 << 15) & 0xefc60000)) & 0xfffe0000)
    y1 = y2 & 0x7f
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 7))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 14))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 21))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & 0xf0000000)
    y0 = (y1 & 0xffe00000)
    y0 |= (((y0 >> 11) ^ y1) & 0x001ffc00)
    y0 |= (((y0 >> 11) ^ y1) & 0x3ff)

    return y0


def test_untemper():
    for i in range(10 ** 4):
        raw = temper(i)
        recovered = untemper(raw)
        if i != recovered:
            print("Untemper algorithm is Wrong!")
            raise RuntimeError


if __name__ == "__main__":
    main()

