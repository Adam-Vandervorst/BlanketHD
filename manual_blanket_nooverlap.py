from bhv.np import NumPyPacked64BHV as BHV

from statistics import fmean, pstdev
from random import shuffle
from math import ceil


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


def policy(hvs: list[BHV], blankets: int) -> list[BHV]:
    chunksize = ceil(N/blankets)
    print("chunksize:", chunksize)
    return [BHV.majority(hvs[i:i+chunksize]) for i in range(0, N, chunksize)]


for nbs in range(1, 20):
    print("blankets:", nbs)

    bs = policy(hvs, nbs)

    bers = [[hv.bit_error_rate(b) for b in bs] for hv in hvs]
    nbers = [[hv.bit_error_rate(b) for b in bs] for hv in nhvs]

    mins = [min(bers[i][bn] for bn in range(nbs)) for i in range(N)]
    nmins = [min(nbers[i][bn] for bn in range(nbs)) for i in range(N)]

    print("positive examples")
    print(" furthest from noise:", BHV.frac_to_std(min(mins) - .5, relative=True))
    print(" average:", BHV.frac_to_std(fmean(mins) - .5, relative=True))
    print(" closest to noise:", BHV.frac_to_std(max(mins) - .5, relative=True))

    print("negative examples")
    print(" furthest from noise:", BHV.frac_to_std(min(nmins) - .5, relative=True))
    print(" average:", BHV.frac_to_std(fmean(nmins) - .5, relative=True))
    print(" closest to noise:", BHV.frac_to_std(max(nmins) - .5, relative=True))

    print(fmean([(BHV.frac_to_std(min(b.bit_error_rate(hv) for b in bs) - .5, relative=True) >= 9) == (i < N)
                 for i, hv in enumerate(hvs + nhvs)]))
