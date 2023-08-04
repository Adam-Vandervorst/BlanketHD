from bhv.lookup import StoreList
# from bhv.native import NativePackedBHV as BHV
from bhv.np import NumPyPacked64BHV as BHV


# https://www.sciencedirect.com/science/article/pii/0166218X9390045P/pdf?md5=e39c66ca8fd845fc3f2fe5cae99f4e26&pid=1-s2.0-0166218X9390045P-main.pdf
# fig 4
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
hyperedges = [
    ([1], [2, 3]),
    ([1], [4, 5]),
    ([2], [3, 6]),
    ([4, 5], [3, 7]),
    ([7], [6, 8]),
    ([9], [8])
]

def convert(ns, hs, initial=None):
    hvs = initial or {n: BHV.rand() for n in ns}
    binds = []

    for xs, ys in hs:
        xb = BHV.majority([hvs[x] for x in xs])
        yb = BHV.majority([hvs[y] for y in ys])
        binds.append(xb ^ yb.permute(1))
    return hvs, BHV.majority(binds)


hvs, Ghv = convert(nodes, hyperedges)

store = StoreList(hvs)

step1 = (Ghv ^ hvs[1]).permute(-1)
step1_results = list(store.related(step1))
print(step1_results)

step2 = (Ghv ^ BHV.majority([hvs[r] for r in step1_results])).permute(-1)
step2_results = list(store.related(step2, 4))
print(step2_results)

step3 = (Ghv ^ BHV.majority([hvs[r] for r in step2_results])).permute(-1)
step3_results = list(store.related(step3, 4))
print(step3_results)
# detected three-step neighbors 6 and 8 via paths 1-5-7-6 and 1-5-7-8

step1 = (Ghv ^ hvs[1]).permute(-1)
step2 = (Ghv ^ step1).permute(-1)
step3 = (Ghv ^ step2).permute(-1)
step3_results = list(store.related(step3, 4))
print(step3_results)
# doesn't work if you don't do intermediate clean up
