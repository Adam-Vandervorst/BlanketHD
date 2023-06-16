from bhv.np import NumPyPacked64BHV as BHV
# from bhv.native import NativePackedBHV as BHV

from random import shuffle
from statistics import fmean, pstdev
from math import ceil


maj_ber_index = [BHV.maj_ber(i) for i in range(1, 2_000)]
def ber_maj(ber: float) -> int:
    return next(i for i, v in enumerate(maj_ber_index) if v <= ber)


class BlanketPolicy:
    def __init__(self, recovery: float, margin: float):
        self.recovery = recovery
        self.margin = margin

    def nblankets(self, nhvs: int) -> int:
        raise NotImplementedError()

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        raise NotImplementedError()

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        raise NotImplementedError()


class NonOverlapping(BlanketPolicy):
    def nblankets(self, n: int) -> int:
        return ceil(n / ber_maj(BHV.std_to_frac(self.recovery + self.margin)))

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        n = len(hvs)
        chunksize = ceil(n/self.nblankets(n))
        return [BHV.majority(hvs[i:i+chunksize]) for i in range(0, n, chunksize)]

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        return BHV.frac_to_std(min(b.bit_error_rate(target) for b in bs), invert=True) >= self.recovery


class PerfectOverlap(BlanketPolicy):
    def __init__(self, recovery: float, redundancy: int = 2):
        super().__init__(recovery, 0)
        self.redundancy = redundancy

    def nbase(self, n: int) -> int:
        return NonOverlapping(self.recovery, 0).nblankets(n)

    def nblankets(self, n: int) -> int:
        return self.redundancy*self.nbase(n)

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        n = len(hvs)
        chunksize = ceil(n / self.nbase(n))
        offset = chunksize // self.redundancy
        hvs = hvs + hvs[:chunksize + 1]
        bs = []
        for i in range(0, N, chunksize):
            for r in range(self.redundancy):
                bs.append(BHV.majority(hvs[i + r * offset:i + chunksize + r * offset + 1]))
        return bs

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        bers = [b.bit_error_rate(target) for b in bs]
        bers = bers + bers[:self.redundancy]
        return BHV.frac_to_std(min(fmean(bers[i:i + self.redundancy]) for i in range(len(bers))), invert=True) >= self.recovery


class NonOverlappingBindRedundant(BlanketPolicy):
    def __init__(self, recovery: float, redundancy: int = 2, permutation=1):
        super().__init__(recovery, 0)
        self.redundancy = redundancy
        self.permutation = permutation
        self.bases = BHV.nrand(redundancy)

    def nbase(self, n: int) -> int:
        return NonOverlapping(self.recovery, 0).nblankets(n)

    def nblankets(self, n: int) -> int:
        return self.redundancy*self.nbase(n)

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        n = len(hvs)
        chunksize = ceil(n / self.nbase(n))
        bs = []
        for i in range(0, N, chunksize):
            for base in self.bases:
                bs.append(BHV.majority([base ^ hv for hv in hvs[i:i + chunksize]]))
        return bs

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        ts = [target ^ base for base in self.bases]
        bers = [fmean([bs[i*self.redundancy + j].bit_error_rate(t) for j, t in enumerate(ts)]) for i in range(len(bs)//self.redundancy)]
        return BHV.frac_to_std(min(bers), invert=True) >= 3


N = 1000
if True:
    hvs = BHV.nrand(N)
    nhvs = BHV.nrand(N)
else:
    s = BHV.rand()

    hvs = []
    for _ in range(N):
        hvs.append(s)
        s = s.flip_pow(2)
    shuffle(hvs)

    nhvs = []
    for _ in range(N):
        nhvs.append(s)
        s = s.flip_pow(2)
    shuffle(nhvs)

# policy = NonOverlapping(recovery=5, margin=2)
policy = NonOverlappingBindRedundant(recovery=5, redundancy=2)
# policy = PerfectOverlap(recovery=3.5, redundancy=2)


bs = policy.blankets(hvs)
nbs = len(bs)

print("blankets:", nbs)

print(fmean([policy.accept(bs, hv) == (i < N)
             for i, hv in enumerate(hvs + nhvs)]))
