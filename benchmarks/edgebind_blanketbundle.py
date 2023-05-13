from time import monotonic
from statistics import fmean, pstdev
from random import sample
from multiprocessing import Pool


import networkx as nx
from bhv.np import NumPyPacked64BHV as BHV
# from bhv.np import NumPyBoolBHV as BHV


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


def convert(g: nx.Graph, initial=None, ms=10, red=2):
    hvs = initial or {n: BHV.rand() for n in g.nodes}

    with Pool() as p:
        binds = p.starmap(BHV.__xor__, [(hvs[x], hvs[y]) for x, y in g.edges])
        blankets = p.map(BHV.majority, [sample(binds, int(red*len(binds)/ms)) for _ in range(ms)])
    return hvs, blankets


conversion_times = []
scoring_times = []
avg_overshoot = []
avg_undershoot = []

for i in range(5):
    print("repetition", i)
    G = nx.erdos_renyi_graph(1000, 0.03)
    t0 = monotonic()
    RED = 2
    B = 1000//(30//RED)
    hvs, blankets = convert(G, ms=B, red=RED)
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
Workstation 8 cores
5 repetitions

100 nodes
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

1000/15 redundancy 2 blankets (checking 1 in 10)
conversion time: 2.72682489764411 +- 0.04742734934242383
scoring time: 4.615515147196129 +- 0.17808535994692343
overshoot loss: 0.4832444826882484 +- 0.014321876298373441
undershoot loss: 0.5522187451599556 +- 0.012364810368286287
"""
