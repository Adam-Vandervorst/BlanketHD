from bhv.native import NativePackedBHV as BHV

from statistics import fmean, pstdev, geometric_mean
from random import shuffle
from math import ceil

RED = 3

N = 1000

if False:
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


def policy(hvs: list[BHV], nblankets: int) -> list[BHV]:
    chunksize = ceil(N/nblankets)
    offset = chunksize//RED
    print("responsible chunksize:", offset)
    hvs = hvs + hvs[:chunksize+1]
    bs = []
    for i in range(0, N, chunksize):
        for r in range(RED):
            bs.append(BHV.majority(hvs[i + r*offset:i+chunksize + r*offset+1]))
    return bs


def score(blankets: list[BHV], target: BHV) -> float:
    bers = [b.bit_error_rate(target) for b in blankets]
    bers = bers + bers[:RED]
    return min(fmean(bers[i:i+RED]) for i in range(len(bers)))


for nbs in range(1, 10):
    print("blankets:", nbs, nbs*RED)

    bs = policy(hvs, nbs)

    bers = [score(bs, hv) for hv in hvs]
    nbers = [score(bs, hv) for hv in nhvs]

    print("positive examples")
    print(" furthest from noise:", BHV.frac_to_std(min(bers) - .5, relative=True))
    print(" average:", BHV.frac_to_std(fmean(bers) - .5, relative=True))
    print(" closest to noise:", BHV.frac_to_std(max(bers) - .5, relative=True))

    print("negative examples")
    print(" furthest from noise:", BHV.frac_to_std(min(nbers) - .5, relative=True))
    print(" average:", BHV.frac_to_std(fmean(nbers) - .5, relative=True))
    print(" closest to noise:", BHV.frac_to_std(max(nbers) - .5, relative=True))

    print(fmean([(BHV.frac_to_std(min(b.bit_error_rate(hv) for b in bs) - .5, relative=True) >= 4) == (i < N)
                 for i, hv in enumerate(hvs + nhvs)]))
