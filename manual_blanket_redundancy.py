# from bhv.np import NumPyPacked64BHV as BHV
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
    print(" furthest from noise:", BHV.frac_to_std(min(bers), invert=True))
    print(" average:", BHV.frac_to_std(fmean(bers), invert=True))
    print(" closest to noise:", BHV.frac_to_std(max(bers), invert=True))

    print("negative examples")
    print(" furthest from noise:", BHV.frac_to_std(min(nbers), invert=True))
    print(" average:", BHV.frac_to_std(fmean(nbers), invert=True))
    print(" closest to noise:", BHV.frac_to_std(max(nbers), invert=True))

    print(fmean([(BHV.frac_to_std(min(b.bit_error_rate(hv) for b in bs), invert=True) >= 4) == (i < N)
                 for i, hv in enumerate(hvs + nhvs)]))

"""
red 2

positive examples
 furthest from noise: 9.468601741826106
 average: 6.4571113005567895
 closest to noise: 4.342077578223638
negative examples
 furthest from noise: 3.2040776022515445
 average: 1.2653233907595052
 closest to noise: -0.8507378461150665

no overlap
 
positive examples
 furthest from noise: 12.285980323116263
 average: 9.154116000893396
 closest to noise: 5.457980467283662
negative examples
 furthest from noise: 3.95537855726225
 average: 1.750995264000096
 closest to noise: 0.3977475644174291
"""