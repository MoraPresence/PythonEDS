import random
from collections import namedtuple

h_ = 0
e = 0
alpha = 3
q = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
k = 0
p = 0x8000000000000000000000000000000000000000000000000000000000000431
a = 0x7
b = 0x5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E
m = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
xP = 0x2
yP = 0x8E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8
d = 0x7A929ADE789BB9BE10ED359DD39A72C11B60961F49397EEE1D19CE9891EC3B28
xQ = 0x7F2B49E270DB6D90D8595BEC458B50C58585BA1D4E9B788F6689DBD8E56FD80B
yQ = 0x26F1B489D6701DD185C8413A977B3CBBAF64D1C593D26627DFFB101A87FF77DA

Point = namedtuple("Point", "x y")
O = 'Origin'

class ECPoint(Point):
    def valid(self, P):
        if P == O:
            return True
        else:
            return (
                (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and
                0 <= P.x < p and 0 <= P.y < p)


    def inv_mod_p(self, x):
        if x % p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, p-2, p)

    def ec_inv(self, P):
        if P == O:
            return P
        return Point(P.x, (-P.y)%p)

    def ec_add(self, P, Q):
        if not (self.valid(P) and self.valid(Q)):
            raise ValueError("Invalid inputs")
        if P == O:
            result = Q
        elif Q == O:
            result = P
        elif Q == self.ec_inv(P):
            result = O
        else:
            if (P.x == Q.x and P.y == Q.y):
                dydx = (3 * P.x**2 + a) * self.inv_mod_p(2 * P.y)
            else:
                dydx = (Q.y - P.y) * self.inv_mod_p(Q.x - P.x)
            x = (dydx**2 - P.x - Q.x) % p
            y = (dydx * (P.x - x) - P.y) % p
            result = Point(x, y)
        assert self.valid(result)
        return result

    def bits(self, n):
        while n:
            yield n & 1
            n >>= 1

    def double_and_add(self, n, x):
        result = O
        addend = x

        for bit in self.bits(n):
            if bit == 1:
                result = self.ec_add(result, addend)
            addend = self.ec_add(addend, addend)
        return result

if alpha % q == 0:e = 1

e = 0x2DFBC1B372D89A1188C09C52E0EEC61FCE52032AB1022E8E67ECE6672B043EE5
s = 0
while(True):
    #k = random.uniform(0, q)
    k = 0x77105C9B20BCD3122823C8CF6FCC7B956DE33814E95B7FE64FED924594DCEAB3

    C = ECPoint(0,0)
    P = ECPoint(xP, yP)
    C = C.double_and_add(k, P)
    r = C.x % q
    if r != 0:
        s = (r*d + k*e)%q
    if s != 0: break




print(C)
print(r)
print(s)

