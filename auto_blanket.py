# from bhv.np import NumPyPacked64BHV as BHV
from bhv.native import NativePackedBHV as BHV

from random import shuffle, sample, random
from statistics import fmean, pstdev, geometric_mean
from math import ceil


maj_ber_index = [BHV.maj_ber(i) for i in range(1, 2_000)]
def ber_maj(ber: float) -> int:
    return next(i for i, v in enumerate(maj_ber_index) if v <= ber)


class BlanketPolicy:
    def expected_overlap(self, n: int) -> float:
        raise NotImplementedError()

    def nblankets(self, n: int) -> int:
        raise NotImplementedError()

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        raise NotImplementedError()

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        raise NotImplementedError()


# ------------------ ------------------ ------------------ ------------------ ----| bundle blanket
# ................................................................................| input vector
class NonOverlapping(BlanketPolicy):
    def __init__(self, recovery: float, margin: float):
        self.recovery = recovery
        self.margin = margin

    def expected_overlap(self, n: int) -> float:
        return 1

    def nblankets(self, n: int) -> int:
        return ceil(n / ber_maj(BHV.std_to_frac(self.recovery + self.margin)))

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        n = len(hvs)
        chunksize = ceil(n/self.nblankets(n))
        return [BHV.majority(hvs[i:i+chunksize]) for i in range(0, n, chunksize)]

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        return BHV.frac_to_std(min(b.bit_error_rate(target) for b in bs), invert=True) >= self.recovery


# -------- ------------------ ------------------ ------------------ --------------| bundle blanket layer 1
# ------------------ ------------------ ------------------ ------------------ ----| bundle blanket layer 1
# ................................................................................| input vector
class PerfectOverlap(BlanketPolicy):
    def __init__(self, recovery: float, redundancy: int = 2):
        self.recovery = recovery
        self.redundancy = redundancy

    def expected_overlap(self, n: int) -> float:
        return self.redundancy

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


# ------------------ ------------------ ------------------ ------------------ ----|  blanket to corresponding basis 1
# ................................................................................|  input bound with basis vector 1
# ------------------ ------------------ ------------------ ------------------ ----|  blanket to corresponding basis 2
# ................................................................................|  input bound with basis vector 2
# ------------------ ------------------ ------------------ ------------------ ----|  blanket to corresponding basis 3
# ................................................................................|  input bound with basis vector 3
class NonOverlappingBindRedundant(BlanketPolicy):
    def __init__(self, recovery: float, redundancy: int = 2, permutation=1):
        self.recovery = recovery
        self.redundancy = redundancy
        self.permutation = permutation
        self.bases = BHV.nrand(redundancy)

    def expected_overlap(self, n: int) -> float:
        return self.redundancy

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


# =----------                         -----                             ------   -| bundle blankets
#         ---------------------- ----                                             |   ||
#    --                -----------------         -----   ---------------------    |   ||
# ----------------   ------------       ---------------------------------- -------|   ||
# ................................................................................| input vector
class Chaotic(BlanketPolicy):
    def __init__(self, sizes: list[float]):
        self.sizes = sizes

    def expected_overlap(self, n: int) -> float:
        return sum(s*n for s in self.sizes)/n

    def nblankets(self, n: int) -> int:
        return len(self.sizes)

    def blankets(self, hvs: list[BHV]) -> list[BHV]:
        n = len(hvs)
        return [BHV.majority(sample(hvs, k=int(size*n))) for size in self.sizes]

    def accept(self, bs: list[BHV], target: BHV) -> bool:
        return BHV.frac_to_std(min([b.bit_error_rate(target) for s, b in zip(self.sizes, bs)]), invert=True) >= 3


N = 1000

initialize = "orthogonal"
if initialize == "orthogonal":
    hvs = BHV.nrand(N)
    nhvs = BHV.nrand(N)
elif initialize == "path":
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
elif initialize == "composite":
    d = 4
    dd = d*d
    pool = BHV.nrand(N//d)

    hvs = [BHV.representative(sample(pool, k=N//d)) for i in range(N)]
    nhvs = [BHV.representative(sample(pool, k=N//d)) for i in range(N)]

# policy = NonOverlapping(recovery=5, margin=2)
policy = NonOverlappingBindRedundant(recovery=5, redundancy=3)
# policy = PerfectOverlap(recovery=5, redundancy=2)
# policy = Chaotic([.9 for _ in range(50)])


bs = policy.blankets(hvs)
nbs = len(bs)

print("blankets:", nbs)

print(fmean([policy.accept(bs, hv) == (i < N)
             for i, hv in enumerate(hvs + nhvs)]))
