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

    return hvs, rec(())


hvs, Ghv = convert(nodes, hyperedges)

index_to_name = lambda x: x+1

starting11 = ((Ghv ^ hvs[1]).permute(-1) ^ hvs[1]).permute(-2)
starting11_results = starting11.within_std(hvs.values(), -4, True)
print(*map(index_to_name, starting11_results))

starting12 = ((Ghv ^ hvs[1]).permute(-1) ^ hvs[2]).permute(-2)
starting12_results = starting12.within_std(hvs.values(), -4, True)
print(*map(index_to_name, starting12_results))
