from bhv.lookup import StoreList
from bhv.native import NativePackedBHV as BHV


# https://link.springer.com/article/10.1007/s00454-012-9469-6 page 258
nodes = [1, 2, 3, 4, 5, 6]
hyperedges = [
    ([1], [2]),
    ([2], [3]),
    ([3], [1]),
    ([2, 3], [4, 5]),
    ([3, 5], [6])
]


def convert(ns, hs, initial=None):
    hvs = initial or {n: BHV.rand() for n in ns}
    binds = []

    for xs, ys in hs:
        xb = BHV.ZERO
        for x in xs:
            xb = xb ^ hvs[x]
        # xb = BHV.majority(hvs[x] for x in xs)
        yb = BHV.majority(hvs[y] for y in ys)
        binds.append(xb ^ yb.permute(1))
    return hvs, BHV.majority(binds)


hvs, Ghv = convert(nodes, hyperedges)

store = StoreList(hvs)

nbs23 = (Ghv ^ hvs[2] ^ hvs[3]).permute(-1)
print(list(store.related(nbs23)))


nbs23 = (Ghv ^ BHV.majority([hvs[3], hvs[2]])).permute(-1)
print(list(store.related(nbs23, threshold=3)))
