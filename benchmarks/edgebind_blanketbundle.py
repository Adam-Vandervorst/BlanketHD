from time import monotonic
from statistics import fmean, pstdev
from random import sample
from multiprocessing import Pool


import networkx as nx
from bhv.np import NumPyPacked64BHV as BHV
# from bhv.np import NumPyBoolBHV as BHV


#  nbsf has type nx.Node -> [nx.Node]
#  and the oracle satisfying this is g.neighbors
def score_undirected_nbs(g: nx.Graph, nbsf, check_frac=.1):
    counts = []
    overs = []
    unders = []
    to_check = sample(list(g.nodes), int(len(g)*check_frac))

    with Pool() as p:
        results = p.map(nbsf, to_check)

    for n, result in zip(to_check, results):
        truth = set(g.neighbors(n))
        predicted = set(result)
        count = len(truth)
        over = len(predicted - truth)
        under = len(truth - predicted)
        counts.append(count)
        overs.append(over)
        unders.append(under)
    return counts, overs, unders


def convert(g: nx.Graph, initial=None, nblankets=10, redundancy=2):
    hvs = initial or {n: BHV.rand() for n in g.nodes}

    with Pool() as p:
        binds = p.starmap(BHV.__xor__, [(hvs[x], hvs[y]) for x, y in g.edges])
        blankets = p.map(BHV.majority, [sample(binds, int(redundancy*len(binds)/nblankets)) for _ in range(nblankets)])
    return hvs, blankets


N = 1000
Ef = 0.03
RED = 2
B = N//(30//RED)  # 30 is the capacity of a majority bundle used


conversion_times = []
scoring_times = []
avg_overshoot = []
avg_undershoot = []

for i in range(5):
    print("repetition", i)
    G = nx.erdos_renyi_graph(N, Ef)
    t0 = monotonic()
    hvs, blankets = convert(G, nblankets=B, redundancy=RED)
    ct = monotonic() - t0
    print("conversion time:", ct)
    conversion_times.append(ct)

    def nbs(n):
        hv = hvs[n]
        nbs_options = [blanket ^ hv for blanket in blankets]
        return [n_ for n_ in G.nodes if
                sum(not hvs[n_].unrelated(nbs_option, 3) for nbs_option in nbs_options) >= RED]


    t0 = monotonic()
    cs, os, us = score_undirected_nbs(G, nbs)
    st = monotonic() - t0
    print("scoring time:", st)
    scoring_times.append(st)
    mcs = fmean(cs)
    print("stats:", mcs, pstdev(cs))
    mos = fmean(os)
    mus = fmean(us)
    print("scores:", mos, mus)
    avg_overshoot.append(mos/mcs)
    avg_undershoot.append(mus/mcs)


print("conversion time:", fmean(conversion_times), "+-", pstdev(conversion_times))
print("scoring time:", fmean(scoring_times), "+-", pstdev(scoring_times))
print("overshoot loss:", fmean(avg_overshoot), "+-", pstdev(avg_overshoot))
print("undershoot loss:", fmean(avg_undershoot), "+-", pstdev(avg_undershoot))


"""
Adam Workstation 8 cores

1000 nodes
1 "blanket" (NOTE this is doing a very large bundle, use NumPyBoolBHV)
conversion time: 0.41756714361254127 +- 0.0639423438148542
scoring time: 18.3407090557972 +- 0.3667289361444694
overshoot loss: 1.4830413311629933 +- 0.01862748160240708
undershoot loss: 0.9156151054085824 +- 0.0008664566438166838

10 disjoint blankets
conversion time: 5.286508035403676 +- 0.009888001521766079
scoring time: 0.7203056167811155 +- 0.028054543306225213
overshoot loss: 0.8763651593649275 +- 0.020374035578414305
undershoot loss: 0.8555179588353592 +- 0.006161792551931035

1000//(30//2) blankets (checking 1 in 10)
conversion time: 2.72682489764411 +- 0.04742734934242383
scoring time: 4.615515147196129 +- 0.17808535994692343
overshoot loss: 0.4832444826882484 +- 0.014321876298373441
undershoot loss: 0.5522187451599556 +- 0.012364810368286287

AWS c6i.large 2 cores
1000//(30//2) blankets (checking 1 in 10)
conversion time: 12.228359039600026 +- 0.12517443612193752
scoring time: 50.87219557479998 +- 0.1338535056834851
overshoot loss: 0.4684689726364574 +- 0.015055239250897216
undershoot loss: 0.5702441709158104 +- 0.008900834538223358

AWS c6i.x16large 64 cores
1000//(30//2) blankets (checking 1 in 10)
conversion time: 0.9360306159999994 +- 0.012868246615325736
scoring time: 2.0433540976000133 +- 0.015534015157973488
overshoot loss: 0.46209885034199116 +- 0.007352991359913596
undershoot loss: 0.5704420880132461 +- 0.00906461941805357


AWS c6in.metal 128 cores
1000//(30//2) blankets (checking 1 in 10)
TODO
"""
