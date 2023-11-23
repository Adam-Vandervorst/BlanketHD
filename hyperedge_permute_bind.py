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

index_to_name = lambda x: x+1

starting11 = ((Ghv ^ hvs[1]) ^ hvs[1].permute(1)).permute(-2)
starting11_results = starting11.within_std(hvs.values(), -4, True)
print(*map(index_to_name, starting11_results))

starting12 = ((Ghv ^ hvs[1]) ^ hvs[2].permute(1)).permute(-2)
starting12_results = starting12.within_std(hvs.values(), -4, True)
print(*map(index_to_name, starting12_results))
