# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

'''
import gmpy2
import math


class bad_rsa:
    def __init__(self, N):
        self.N = N
        self.computePrime()

    def computePrime(self):
        for i in range (1, 2**20):
            self.A = gmpy2.isqrt(self.N) + i
            self.calcX()
            if self.verify():
                print("found it!")
                print(self.p)
                break

    def calcX(self):
        Asquared = gmpy2.mul(self.A, self.A)
        remainder = gmpy2.sub(Asquared, self.N)
        self.x  = gmpy2.isqrt_rem(remainder)[0]

    def verify(self):
        self.p = gmpy2.sub(self.A, self.x)
        self.q = gmpy2.add(self.A ,self.x)
        if gmpy2.mul(self.p, self.q) == self.N:
            return True
        else:
            return False


#problem 1
prob1 = gmpy2.mpz('17976931348623159077293051907890247336179769789423065727343008115' +
                   '77326758055056206869853794492129829595855013875371640157101398586' +
                   '47833778606925583497541085196591615128057575940752635007475935288' +
                   '71082364994994077189561705436114947486504671101510156394068052754' +
                   '0071584560878577663743040086340742855278549092581')
#problem 2
prob2 = gmpy2.mpz('6484558428080716696628242653467722787263437207069762630604390703787' +
                  '9730861808111646271401527606141756919558732184025452065542490671989' +
                  '2428844841839353281972988531310511738648965962582821502504990264452' +
                  '1008852816733037111422964210278402893076574586452336833570778346897' +
                  '15838646088239640236866252211790085787877')

a = bad_rsa(prob1)
input("Enter Key")

'''