# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 自己写的算了半天算不出来，还是参考writeUp吧
# 怪不得算不出来，原来是因为没有模p啊
# 参考了网上的，还是算得很慢。。。
# gmpy2 https://gmpy2.readthedocs.org/en/latest/mpz.html#mpz-methods

import gmpy2


def main():
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
    g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
    h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
    file_name = "hash_table"

    # 性能差异太明显了，gmpy2计算好快好快~~
    # hash_table = compute_hash_table(h, g, p)
    # write_to_file(hash_table, file_name)

    hash_table = get_hash_table(file_name)
    (x0, x1) = find_solution(g, p, hash_table)
    x = (x0 * gmpy2.mpz(2 ** 20) + x1) % p
    print(x)
    # x = (((357984 * 2**20) + 787046)% p)
    # 375374217830


def compute_hash_table(h, g, p):
    """
    :param h: 22
    :param g: 43
    :param p: 35
    :return: {mpz(8): 2, mpz(1): 3, mpz(29): 1, mpz(22): 0}
    """
    hash_table = dict()
    for x1 in range(2 ** 20 + 1):
        denominv = pow(g, x1, p)  # 计算分母
        denom = gmpy2.invert(denominv, p)  # 计算1/分母
        tval = gmpy2.mul(h, denom)  # 计算h * 1/分母
        res = gmpy2.f_mod(tval, p)  # 对p求模

        hash_table.setdefault(res, x1)

    return hash_table


def write_to_file(hash_table, file_name):
    """
    :param hash_table: {mpz(8): 2, mpz(1): 3, mpz(29): 1, mpz(22): 0}
    """
    with open(file_name, 'w+') as f:
        for key, value in hash_table.items():
            f.write("{0}:{1}\n".format(key, value))


def find_solution(g, p, hash_table):
    """
    :param g: 22
    :param p: 35
    :param hash_table: {mpz(8): mpz(2), mpz(1): mpz(3), mpz(29): mpz(1), mpz(22): 0}
    :return: (x0, x1)
    """
    for x0 in range(2 ** 20 + 1):
        result = pow(g, (2 ** 20) * x0, p)
        if result in hash_table:
            return (x0, hash_table[result])


def get_hash_table(file_name):
    """
    :param file_name: hash_table
    :return: {mpz(8): mpz(2), mpz(1): mpz(3), mpz(29): mpz(1), mpz(22): mpz(0)}
    """
    hash_table = dict()
    with open(file_name, 'rU') as f:
        lines = f.readlines()

    for data in lines:
        data = data.strip().split(':')
        (key, value) = (data[0], data[1])
        hash_table.setdefault(gmpy2.mpz(key), gmpy2.mpz(value))

    return hash_table


if __name__ == "__main__":
    main()

