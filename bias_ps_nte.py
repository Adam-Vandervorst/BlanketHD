from bhv.np import NumPyBoolBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("graphs/InteractiveDisneyStrategy.json", "property_graph")


def bias_ps(s, ps, o, pw=1):
    mps = BHV.majority(ps)
    s_ = mps.select(s.flip_pow_on(pw), s.flip_pow_off(pw))
    o_ = mps.select(o.flip_pow_off(pw), o.flip_pow_on(pw))
    return s_, o_


def convert(nte: HDict, initial=None, pw=1):
    hvs = initial or {n['id']: BHV.rand() for n in nte.find_nodes()}

    for s, ps, o in squash(nte.triples(), axis=1):
        hvs[s], hvs[o] = bias_ps(hvs[s], [hvs[p] for p in ps], hvs[o], pw)

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
hvs = convert(NTE, pw=1)

print("predicting properties")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(ps)
    print([p for p in hvs if p != s and hvs[s].bias_rel(hvs[o], hvs[p]) > .55])
print()
print("predicting neighbors")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(*pos, sep='\t')
        print(*[(p, [o for o in os if hvs[s].bias_rel(hvs[o], hvs[p]) > .50]) for (p, os) in pos], sep='\t')
