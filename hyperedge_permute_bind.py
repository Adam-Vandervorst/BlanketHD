from bhv.lookup import StoreList
from bhv.native import NativePackedBHV as BHV

# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/the-representation-of-rules/
nodes = [1, 2, 3, 4]
hyperedges = [
    (1, 1, 1),
    (1, 2, 3),
    (3, 4, 4)
]


def convert(ns, hs, initial=None):
    hvs = initial or {n: BHV.rand() for n in ns}
    binds = []

    for xs in hs:
        xb = BHV.ZERO
        for i in reversed(range(len(xs))):
            xb = (xb ^ hvs[xs[i]].permute(i))

        binds.append(xb)
    return hvs, BHV.majority(binds)


hvs, Ghv = convert(nodes, hyperedges)

store = StoreList(hvs)

starting11 = ((Ghv ^ hvs[1]) ^ hvs[1].permute(1)).permute(-2)
starting11_results = list(store.related(starting11))
print(starting11_results)

starting12 = ((Ghv ^ hvs[1]) ^ hvs[2].permute(1)).permute(-2)
starting12_results = list(store.related(starting12))
print(starting12_results)
