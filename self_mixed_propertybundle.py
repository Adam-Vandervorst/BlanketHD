from random import shuffle

from bhv.np import NumPyBoolBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("graphs/InteractiveDisneyStrategy.json", "property_graph")


def convert(nte: HDict, initial=None, iterations=1, pw=1):
    """
    Supports (s, ?, o) and (s, p, ?) queries
    Update rule: v_{n+1} = v_n + \sigma(\pi(w, e) | e \in I(v, w), w \in N(v))\cdot\epsilon
    """
    hvs = initial or {n['id']: BHV.rand() for n in nte.find_nodes()}

    for _ in range(iterations):
        for s in nte.find_nodes():
            s = s['id']
            pos = BHV.majority([hvs[p] ^ hvs[o] for p, o in nte.triples(s=s)])
            hvs[s] = hvs[s].select_rand2(pos, pw)

    return hvs


hvs = convert(NTE, pw=1)

print("predicting properties (s, ?, o)")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(ps)
    print([p for p in hvs if p != s and not (hvs[s] ^ hvs[o]).unrelated(hvs[p], 3)])
print()
print("predicting neighbors (s, p, ?)")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(*pos, sep='\t')
        print(*[(p, [o for o in os if not (hvs[s] ^ hvs[p]).unrelated(hvs[o], 3)]) for (p, os) in pos], sep='\t')
