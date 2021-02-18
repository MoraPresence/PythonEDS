import CECPoint
import random

class ECP:
    q = 0
    m = 0
    pointArgs = 0

    def __init__(self, q, m, pointArgs):
        self.q = q
        self.m = m
        self.pointArgs = pointArgs

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

            C = CECPoint.ECPoint.double_and_add(k, P)
            r = C.myP.x % self.q
            if r != 0:
                s = (r * d + k * e) % self.q
            if s != 0: break

        return f"{r};{s}"

    def verify(self, sign, M, Q, P):
        r, s = sign.split(";")
        r = int(r)
        s = int(s)
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

        C = CECPoint.ECPoint(0, 0, P.pointArgs)
        C = C.ec_add(CECPoint.ECPoint.double_and_add(z1, P), CECPoint.ECPoint.double_and_add(z2, Q))
        R = C.myP.x % self.q
        if R == r:
            return True
        else:
            return False