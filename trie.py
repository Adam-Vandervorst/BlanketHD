from bhv.lookup import StoreList
from bhv.native import NativePackedBHV as BHV
# from bhv.symbolic import SymbolicBHV as BHV

# https://www.wolframphysics.org/technical-introduction/basic-form-of-models/the-representation-of-rules/
nodes = [1, 2, 3, 4]
hyperedges = [
    (1, 1, 1),
    (1, 2, 3),
    (3, 4, 4)
]


def convert(ns, hs, initial=None):
    hvs = initial or {n: BHV.rand() for n in ns}
    max_depth = max(map(len, hs))

    def rec(trace):
        if not any(trace == h[:len(trace)] for h in hs): return
        if len(trace) == max_depth: return BHV.ZERO

        m = []
        for n in ns:
            nc = rec(trace + (n,))
            if nc:
                m.append(hvs[n] ^ nc)
        return BHV.majority(m).permute(len(trace))

    # print(rec(()).show(random_id=True))
    return hvs, rec(())


hvs, Ghv = convert(nodes, hyperedges)

store = StoreList(hvs)

starting11 = ((Ghv ^ hvs[1]).permute(-1) ^ hvs[1]).permute(-2)
starting11_results = list(store.related(starting11, 3))
print(starting11_results)

starting12 = ((Ghv ^ hvs[1]).permute(-1) ^ hvs[2]).permute(-2)
starting12_results = list(store.related(starting12, 3))
print(starting12_results)
