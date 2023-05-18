from bhv.np import NumPyBoolBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("../graphs/InteractiveDisneyStrategy.json", "property_graph")


def bias_ps(s, ps, o, pw=1):
    mps = BHV.majority(ps)
    s_ = mps.select(s.flip_pow_on(pw), s.flip_pow_off(pw))
    o_ = mps.select(o.flip_pow_off(pw), o.flip_pow_on(pw))
    return s_, o_


def convert1(nte: HDict, initial=None, pw=1):
    hvs = initial or {n['id']: BHV.rand() for n in nte.find_nodes()}

    for _ in range(16):
        for v in nte.find_nodes():
            v = v['id']
            # v_{n+1} = v_n + \sigma(\pi(w, e) | e \in I(v, w), w \in N(v))\cdot\epsilon
            maj = BHV.majority([hvs[w] ^ hvs[e] for e, w in nte.triples(s=v)])
            hvs[v] = hvs[v].select_rand2(maj, pw)

    return hvs

hvs = convert1(NTE, pw=3)

print("predicting properties")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(ps)
    print([p for p in hvs if p != s and not (hvs[s] ^ hvs[o]).unrelated(hvs[p], 3)])
print()
print("predicting neighbors")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(*pos, sep='\t')
        print(*[(p, [o for o in os if not (hvs[s] ^ hvs[p]).unrelated(hvs[o], 3)]) for (p, os) in pos], sep='\t')
