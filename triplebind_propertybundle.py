from random import shuffle

from bhv.np import NumPyBoolBHV as BHV

from hedit_utils import HDict, squash


# view graph at https://apps.adamv.be/HEdit/?uri=examples/InteractiveDisneyStrategy.json&hide_gray&selected=%5B0%5D&hide_help
NTE = HDict.load_from_path("graphs/InteractiveDisneyStrategy.json", "property_graph")

#   R  S
#   |/  \
# A--->B--->c

# hvps = {A: {R, S}, B: {S}, C: {}}
# hvos = {A: {B}, B: {C}, C: {}}


def convert(nte: HDict, initial=None, iterations=1, pw1=1, pw2=1):
    ns = [s['id'] for s in nte.find_nodes()]
    hvs = initial or {n: BHV.rand() for n in ns}
    hvls = initial or {n: [] for n in ns}
    fhvs = {}

    for s, p, o in nte.triples():
        hvls[p].append(hvs[s].permute(-1) ^ hvs[o].permute(1))

    for n in ns:
        fhvs[n] = BHV.majority(hvls[n])

    return hvs, fhvs

hvs, fhvs = convert(NTE)

print("predicting properties (s, ?, o)")
for s, ps, o in squash(NTE.triples(), axis=1):
    print(s, o)
    print(ps)
    print([p for p in hvs if p != s and not (hvs[s].permute(-1) ^ hvs[o].permute(1)).unrelated(fhvs[p], 3)])
print()
print("predicting neighbors (s, p, ?)")
for s in NTE['data']:
    s = s['id']
    pos = list(squash(NTE.triples(s=s), axis=1))
    if pos:
        print(s)
        print(*pos, sep='\t')
        print(*[(p, [o for o in os if not (hvs[s].permute(-1) ^ fhvs[p]).unrelated(hvs[o].permute(1), 3)]) for (p, os) in pos], sep='\t')

# print()
# print("predicting properties (s, ?, -)")
# for s in NTE['data']:
#     s = s['id']
#     ps = list(set(p for p, _ in NTE.triples(s=s)))
#     if ps:
#         print(s)
#         print(ps)
#         print([p for p in hvps if p != s and not (hvps[s]).unrelated(hvos[p], 3)])
# print()
# print("predicting neighbors (s, -, ?)")
# for s in NTE['data']:
#     s = s['id']
#     os = list(set(o for _, o in NTE.triples(s=s)))
#     if os:
#         print(s)
#         print(os)
#         print([o for o in hvos if o != s and not (hvos[s]).unrelated(hvps[o], 3)])
