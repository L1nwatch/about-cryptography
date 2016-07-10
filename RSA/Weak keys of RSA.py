#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目来源
来自于西电 2016 优研的一道题目, 讨论关于 RSA 弱密钥的问题

# 题目
## 情况描述
There exist values of e and m such that me mod n=m. We call messages m for which me mod n=m unconcealed messages.

## 结论
An issue when choosing e is that there should not be too many unconcealed messages.

## 例子
For instance, let p=19 and q=37. Then n=19*37=703 and φ=18*36=648.
If we choose e=181, then, although gcd(181,648)=1 it turns out that all possible messages m (0≤m≤n-1) are unconcealed
when calculating me mod n.

## 推论
For any valid choice of e there exist some unconcealed messages.
It's important that the number of unconcealed messages is at a minimum.

## 要求
Choose p=1009 and q=3643. Find the sum of all values of e, 1<e<φ(1009,3643) and gcd(e,φ)=1, so that the number of
unconcealed messages for this value of e is at a minimum. Code and run it.
求使得 unconcealed messages 最小值的密钥 e
"""
import gmpy2

__author__ = '__L1n__w@tch'


class MyRSA:
    """
    RSA 类, 给定 p 和 q 之后产生关于 RSA 的一切参数
    """

    def __init__(self, p, q):
        self.p = gmpy2.mpz(p)
        self.q = gmpy2.mpz(q)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

    def print_info(self):
        """
        显示有关该 RSA 的一组相关参数, 包括 p, q, N, phi(N)
        :return:
        """
        print("P = {p}\nQ = {q}\nN = {n}\nphi(N) = {phi}\n".format(p=self.p, q=self.q, n=self.n, phi=self.phi))

    def encrypt(self, m, e):
        """
        加密操作
        :param m: message
        :param e: public key e
        :return: m^e mod n
        """
        message = gmpy2.mpz(m)
        e = gmpy2.mpz(e)
        return gmpy2.powmod(message, e, self.n)

    def decrypt(self, c, d):
        """
        解密操作
        :param c: 被 RSA 加密过的数据
        :param d: 私钥 d
        :return: 解密结果, m
        """
        cipher_text = gmpy2.mpz(c)
        return gmpy2.powmod(cipher_text, d, self.n)

    def generate_e(self):
        """
        产生 e 的生成器
        :return: e, e 满足 1 < e < φ(q,p), 且 gcd(e,φ)=1
        """
        for e in range(2, self.phi):
            if gmpy2.gcd(e, self.phi) == 1:
                yield e

    def is_weak_e(self, e):
        """
        测试给定的 e 是不是弱密钥
        :param e: 公钥 e
        :return: True or False
        """
        for m in range(self.n):
            if self.encrypt(m, e) != m:
                return False
        return True

    def __count_e_unconcealed_message_number(self, e, number):
        """
        遍历的方法来跑出 unconcealed_message 值, 已经被淘汰了.

        给定一个 e, 计算该 e 里面存在的 unconcealed message 数目
        :param e: int()
        :param number: int(), 超过该值时停止计算, 因为肯定不是最小值了
        :return: int()
        """
        counts = 0

        for m in range(self.n):
            if self.encrypt(m, e) == m:
                counts += 1
            if counts >= number:
                return self.n

        return counts

    def get_e_um_result(self, e):
        """
        网上给的一个公式, 好像可以直接计算出来
        [1 + gcd(e - 1, p - 1)] * [1 + gcd(e-1, q-1)]
        :param e: 11
        :return: 9
        """
        return (1 + gmpy2.gcd(e - 1, self.p - 1)) * (1 + gmpy2.gcd(e - 1, self.q - 1))


def weak_example():
    """
    测试题目给的那组数据, 结果发现还真是打印了 0~702
    :return:
    """
    my_rsa = MyRSA(19, 37)
    my_rsa.print_info()
    for i in range(my_rsa.n):
        print(my_rsa.encrypt(i, 181))


def get_weak_e_list(my_rsa):
    """
    给定对应的 rsa 类中存在的弱密钥 e 列表
    :param my_rsa: MyRSA() 实例对象
    :return: 弱密钥 e 列表, 如 [611857, 1223713, 1835569, 2447425, 3059281]
    """
    e_list = my_rsa.generate_e()
    weak_e = list()
    for e in e_list:
        if my_rsa.is_weak_e(e):
            weak_e.append(e)
    return weak_e


def print_weak_e_list(my_rsa):
    """
    打印所有 weak e 的列表
    :param my_rsa: MyRSA() 实例对象
    :return: None
    """
    weak_e = get_weak_e_list(my_rsa)
    print("Weak E: {}".format(weak_e))
    # 最后是要求和么?
    answer = sum(weak_e)
    print("Answer: {}".format(answer))


def get_e_unconcealed_message_dict(my_rsa):
    """
    计算每一个 e 对应的 unconcealed message 数目
    :param my_rsa: MyRSA() 实例对象
    :return: 字典, 表示每一个 e 对应的 unconcealed message, 比如 {515: 9, 5: 15, 7: 49, 521: 15, ...}
    """
    e_list = my_rsa.generate_e()
    e_m_dict = dict()

    for e in e_list:
        e_m_dict[e] = my_rsa.get_e_um_result(e)

    return e_m_dict


def get_min_e_unconcealed_message(my_rsa, first_time=True, min_u_m=None):
    """
    在 get_e_unconcealed_message_dict 函数的基础上改进, 只求最小值
    :param my_rsa: MyRSA() 实例对象
    :param first_time: 标志位, 表明是不是不知道最小的 unconcealed_message 值, 是的话会跑出这个值出来
    :param min_u_m: 最小的 unconcealed_message 值, 如果已知的话需要给出
    :return: int or (list, int), 根据 first_time 来返回不同的结果
    """
    e_list = my_rsa.generate_e()
    min_u_m = min_u_m if not first_time else my_rsa.n
    min_e_list = list()

    for e in e_list:
        # 获取每一个 e 值对应的 unconcealed_message 值
        result = my_rsa.get_e_um_result(e)

        # 如果不知道最小的 unconcealed_message 值这一条语句会把它跑出来
        if first_time and result < min_u_m:
            min_u_m = result

        # 如果知道最小的 m 值则执行这一句, 跑出列表出来
        if not first_time and result == min_u_m:
            min_e_list.append(e)

    if first_time:
        # first_time 则求出最小的 unconcealed_message 值
        return min_u_m
    else:
        # 不是 first_time 则求出对应的 e 列表
        return min_e_list, min_u_m


def test_small_data():
    """
    测试小数据, 题目要求的那个数据有点大, 这个可以作为各个函数的例子来说明
    :return: None
    """
    # 第一步是初始化 RSA
    my_rsa = MyRSA(19, 37)  # 测试小数据的 RSA
    # 打印该 RSA 的相关信息
    my_rsa.print_info()

    # 这个函数打印的是每个 e 对应的 unconcealed_message
    print(get_e_unconcealed_message_dict(my_rsa))  # 打印每一个 e 对应的 unconcealed_message

    # 这个函数获取 unconcealed_message 值, 或者获取 unconcealed_message 值对应的 e 列表
    # 利用 first_time 参数来控制
    min_u_m = get_min_e_unconcealed_message(my_rsa, first_time=True)
    print(min_u_m)

    e_list, m_u_m = get_min_e_unconcealed_message(my_rsa, first_time=False, min_u_m=min_u_m)
    print("Unconcealed Message: {}, Sum_E: {}".format(m_u_m, sum(e_list)))

    # 这个函数用来打印弱密钥 e 列表
    print(get_weak_e_list(my_rsa))


if __name__ == "__main__":
    # weak_example() # 测试题目给的数据
    # test_small_data(); exit()  # 各个函数的使用方法

    # 题目要求的结果
    rsa = MyRSA(1009, 3643)
    rsa.print_info()
    # 之前跑过一次, 知道最小的 unconcealed_message 是 9
    unconcealed_message = get_min_e_unconcealed_message(rsa, first_time=True)
    # unconcealed_message = 9
    result_e_list, min_unconcealed_message = get_min_e_unconcealed_message(rsa, first_time=False,
                                                                           min_u_m=unconcealed_message)
    # 最终结果 Unconcealed Message: 9, Sum_E: 399788195976
    print("Unconcealed Message: {}, Sum_E: {}".format(min_unconcealed_message, sum(result_e_list)))
