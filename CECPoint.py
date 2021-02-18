from collections import namedtuple

Point = namedtuple("Point", "x y")
Zero = Point(0, 0)

pointArgs = namedtuple("pointArgs", "p a b")

class ECPoint:
    myP = 0
    pointArgs = 0

    def __init__(self, x, y, pointArgs):
        self.myP = Point(x, y)
        self.pointArgs = pointArgs

    def _valid(self):
        if self.myP == Zero:
            return True
        else:
            return (
                    (self.myP.y ** 2 - (
                            self.myP.x ** 3 + self.pointArgs.a * self.myP.x + self.pointArgs.b)) % self.pointArgs.p == 0 and
                    0 <= self.myP.x < self.pointArgs.p and 0 <= self.myP.y < self.pointArgs.p)

    def _inv_mod_p(self, x):
        if x % self.pointArgs.p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.pointArgs.p - 2, self.pointArgs.p)

    def _ec_inv(self):
        if self.myP == Zero:
            return self.myP
        return Point(self.myP.x, (-self.myP.y) % self.pointArgs.p)

    def ec_add(self, P, Q):
        if not (P._valid() and Q._valid()):
            raise ValueError("Invalid inputs")
        if P.myP == Zero:
            result = Q
        elif Q.myP == Zero:
            result = P
        elif Q.myP == P._ec_inv():
            result = Zero
        else:
            if (P.myP.x == Q.myP.x and P.myP.y == Q.myP.y):
                dydx = (3 * P.myP.x ** 2 + self.pointArgs.a) * self._inv_mod_p(2 * P.myP.y)
            else:
                dydx = (Q.myP.y - P.myP.y) * self._inv_mod_p(Q.myP.x - P.myP.x)
            x = (dydx ** 2 - P.myP.x - Q.myP.x) % self.pointArgs.p
            y = (dydx * (P.myP.x - x) - P.myP.y) % self.pointArgs.p
            result = ECPoint(x, y, self.pointArgs)
        return result

    def _bits(n):
        while n:
            yield n & 1
            n >>= 1

    def double_and_add(n, x):
        result = ECPoint(0, 0, pointArgs(0, 0, 0))
        addend = x

        for bit in result._bits(n):
            if bit == 1:
                result = result.ec_add(result, addend)
            addend = result.ec_add(addend, addend)
        return result


ECPoint.double_and_add = staticmethod(ECPoint.double_and_add)
ECPoint._bits = staticmethod(ECPoint._bits)
