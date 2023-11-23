# pip install rdflib

from time import monotonic
from statistics import fmean, pstdev

# from bhv.np import NumPyPacked64BHV as BHV
from bhv.native import NativePackedBHV as BHV
from tqdm import tqdm
from rdflib import Graph

g = Graph()

with open("/run/media/adamv/Mass-Storage/Datasets/opencyc/open-cyc.n3") as f:
    g.parse(file=f)

print("examples")
print("-"*22)
for i, (s, p, o) in zip(range(100), g):
    print()
    print(s, p, o, sep="\n")
print("-"*22)

ds = set()
dp = set()
do = set()
for s, p, o in g:
    ds.add(s)
    dp.add(p)
    do.add(o)
print("graph size", len(g))
print("distinct subjects", len(ds))
print("distinct predicates", len(dp))
print("distinct objects", len(do))

s_p_o = {}
for s in ds:
    s_p_o[s] = {}
    for p, o in g.predicate_objects(subject=s, unique=True):
        if p in s_p_o[s]:
            s_p_o[s][p].add(o)
        else:
            s_p_o[s][p] = {o}

psizes = [len(p_o) for p_o in s_p_o.values()]
print("psizes", max(psizes), fmean(psizes), pstdev(psizes))
osizes = [len(o) for p_o in s_p_o.values() for o in p_o.values()]
print("osizes", max(osizes), fmean(osizes), pstdev(osizes))
posizes = [sum(len(o) for o in p_o.values()) for p_o in s_p_o.values()]
print("posizes", max(posizes), fmean(posizes), pstdev(posizes))

ns = ds | dp | do
hv = {n: BHV.rand() for n in tqdm(ns)}
shv = {}

for s, p_o in tqdm(s_p_o.items()):
    hvpos = BHV.majority([hv[p] ^ hv[o] for p, os in p_o.items() for o in os])
    shv[s] = hv[s].select_rand(hvpos)

hv = hv | shv


for _, (s, p_o) in zip(range(50), s_p_o.items()):
    print()
    print(s)
    print([(p, os) for (p, os) in p_o.items()], sep='\t')
    print([(p, [o for o in os if (hv[s] ^ hv[p]).related(hv[o], 3)]) for (p, os) in p_o.items()], sep='\t')
