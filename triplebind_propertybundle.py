from random import shuffle

from bhv.native import NativePackedBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("graphs/InteractiveDisneyStrategy.json", "property_graph")

#   R  S
#   |/  \
# A--->B--->c

# hvps = {A: {R, S}, B: {S}, C: {}}
# hvos = {A: {B}, B: {C}, C: {}}


def convert(nte: HDict, initial=None):
    ns = [s['id'] for s in nte.find_nodes()]
    hvs = initial or {n: BHV.rand() for n in ns}
    hvls = {n: [] for n in ns}

    for s, p, o in nte.triples():
        hvls[p].append(hvs[s].permute(-1) ^ hvs[o].permute(1))

    fhvs = {n: BHV.majority(hvls[n]) for n in ns}

    return hvs, fhvs

hvs, fhvs = convert(NTE)

print("predicting properties (s, ?, o)")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(ps)
    print([p for p in hvs if p != s and (hvs[s].permute(-1) ^ hvs[o].permute(1)).related(fhvs[p], 3)])
print()
print("predicting neighbors (s, p, ?)")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(*pos, sep='\t')
        print(*[(p, [o for o in hvs if (hvs[s].permute(-1) ^ fhvs[p]).related(hvs[o].permute(1), 3)]) for (p, os) in pos], sep='\t')

