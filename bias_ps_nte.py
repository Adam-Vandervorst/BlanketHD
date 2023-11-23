from bhv.native import NativePackedBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("graphs/InteractiveDisneyStrategy.json", "property_graph")


def bias_ps(s, ps, o, frac):
    mps = BHV.majority(ps)
    s_ = mps.select(s.flip_frac_on(frac), s.flip_frac_off(frac))
    o_ = mps.select(o.flip_frac_off(frac), o.flip_frac_on(frac))
    return s_, o_


def measure_bias(x, rel, y):
    rx = x.overlap(rel)
    ry = y.overlap(rel)
    return rx/(rx + ry)


def convert(nte: HDict, initial=None, frac=.5):
    hvs = initial or {n['id']: BHV.rand() for n in nte.find_nodes()}

    for _ in range(200):
        for s, ps, o in squash(nte.triples(), axis=1):
            hvs[s], hvs[o] = bias_ps(hvs[s], [hvs[p] for p in ps], hvs[o], frac)
        for n in hvs:
            hvs[n] = hvs[n] ^ BHV.random(.005)

    return hvs


"""
# Conceptually, you could use pre-calculated vectors like this:
L = BHV.rand()
H = BHV.rand()
def encode(x):
    return L.select_random(H, x)


nodes_and_properties = nte.find_nodes()
nodes = {n['id']: BHV.rand() for n in nodes_and_properties if n['node']}
weights = {n['id']: encode(n['weight']) for n in nodes_and_properties if not n['node']}

precalculated = nodes | weights

hvs = convert(NTE, initial=precalculated, pw=1)
"""
hvs = convert(NTE, frac=.01)

print("predicting properties (s, ?, o)")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(" ", ps)
    print(" ", [(p, measure_bias(hvs[s], hvs[p], hvs[o])) for p in hvs if p != s and p != o and measure_bias(hvs[s], hvs[p], hvs[o]) > 0.55])
print()
print("predicting neighbors (s, -, ?)")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(" ", *pos, sep='\t')
        print(" ", *[(p, [o for o in hvs if measure_bias(hvs[s], hvs[p], hvs[o]) > .55]) for (p, _) in pos], sep='\t')
