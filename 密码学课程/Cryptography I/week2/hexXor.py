# -*- coding: utf-8 -*-
__author__ = 'Lin'


def main():
    hex1 = "bcbf217cb280cf30b2517052193ab979"
    hex2 = "66e94bd4ef8a2c3b884cfa59ca342b2e"
    hex3 = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    result = hexXor(hexXor(hex1, hex2), hex3)
    print(result)


def hexXor(hex1, hex2):
    return hex(int(hex1, 16) ^ int(hex2, 16))[2:]


if __name__ == '__main__':
    main()