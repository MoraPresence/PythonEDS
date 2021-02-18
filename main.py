import random
from collections import namedtuple

Point = namedtuple("Point", "x y")
O = Point(0, 0)

class ECPoint:
    myP = 0
    b = 0x5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E
    p = 0x8000000000000000000000000000000000000000000000000000000000000431
    a = 0x7

    def __init__(self, x, y):
        self.myP = Point(x, y)

    def _valid(self):
        if self.myP == O:
            return True
        else:
            return (
                    (self.myP.y ** 2 - (self.myP.x ** 3 + self.a * self.myP.x + self.b)) % self.p == 0 and
                    0 <= self.myP.x < self.p and 0 <= self.myP.y < self.p)

    def _inv_mod_p(self, x):
        if x % self.p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.p - 2, self.p)

    def _ec_inv(self):
        if self.myP == O:
            return self.myP
        return Point(self.myP.x, (-self.myP.y) % self.p)

    def ec_add(self, P, Q):
        if not (P._valid() and Q._valid()):
            raise ValueError("Invalid inputs")
        if P.myP == O:
            result = Q
        elif Q.myP == O:
            result = P
        elif Q.myP == P._ec_inv():
            result = O
        else:
            if (P.myP.x == Q.myP.x and P.myP.y == Q.myP.y):
                dydx = (3 * P.myP.x ** 2 + self.a) * self._inv_mod_p(2 * P.myP.y)
            else:
                dydx = (Q.myP.y - P.myP.y) * self._inv_mod_p(Q.myP.x - P.myP.x)
            x = (dydx ** 2 - P.myP.x - Q.myP.x) % self.p
            y = (dydx * (P.myP.x - x) - P.myP.y) % self.p
            result = ECPoint(x, y)
        assert result._valid()
        return result

    def _bits(n):
        while n:
            yield n & 1
            n >>= 1

    def double_and_add(n, x):
        result = ECPoint(0, 0)
        addend = x

        for bit in result._bits(n):
            if bit == 1:
                result = result.ec_add(result, addend)
            addend = result.ec_add(addend, addend)
        return result

ECPoint.double_and_add = staticmethod(ECPoint.double_and_add)
ECPoint._bits = staticmethod(ECPoint._bits)

class ECP:
    q = 0
    m = 0
    p = 0
    a = 0
    b = 0

    def __init__(self, q, m, p, a, b):
        self.q = q
        self.m = m
        self.p = p
        self.a = a
        self.b = b

    def signature(self, M, d, P):
        h_ = 0
        e = 0
        alpha = 3
        if alpha % self.q == 0: e = 1
        e = 0x2DFBC1B372D89A1188C09C52E0EEC61FCE52032AB1022E8E67ECE6672B043EE5
        s = 0

        while (True):
            # k = random.uniform(0, q)
            k = 0x77105C9B20BCD3122823C8CF6FCC7B956DE33814E95B7FE64FED924594DCEAB3

            C = ECPoint.double_and_add(k, P)
            r = C.myP.x % self.q
            if r != 0:
                s = (r * d + k * e) % self.q
            if s != 0: break

        return str(r) + str(s)


    def verify(self, sign, M, Q):
        r = int(sign[:77])
        s = int(sign[77:])
        if (r <= 0 and r >= self.q and s <= 0 and s >= self.q):
            return False
        h_ = 0
        e = 0
        alpha = 3
        if alpha % self.q == 0: e = 1
        e = 0x2DFBC1B372D89A1188C09C52E0EEC61FCE52032AB1022E8E67ECE6672B043EE5
        v = pow(e, -1, self.q)
        z1 = s * v % self.q
        z2 = -r * v % self.q


        C = ECPoint(0, 0)
        C = C.ec_add(ECPoint.double_and_add(z1, P), ECPoint.double_and_add(z2, Q))
        R = C.myP.x % self.q
        if R == r:
            return True
        else:
            return False


q = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
m = 0x8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3
p = 0x8000000000000000000000000000000000000000000000000000000000000431
a = 0x7
b = 0x5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E
engine = ECP(q, m, p, a, b)

xP = 0x2
yP = 0x8E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8

P = ECPoint(xP, yP)
d = 0x7A929ADE789BB9BE10ED359DD39A72C11B60961F49397EEE1D19CE9891EC3B28
sign = engine.signature("hi", d , P)
print(sign)

xQ = 0x7F2B49E270DB6D90D8595BEC458B50C58585BA1D4E9B788F6689DBD8E56FD80B
yQ = 0x26F1B489D6701DD185C8413A977B3CBBAF64D1C593D26627DFFB101A87FF77DA
Q = ECPoint(xQ, yQ)

print(engine.verify(sign, "hi", Q))
