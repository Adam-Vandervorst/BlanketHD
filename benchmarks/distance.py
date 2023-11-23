from time import monotonic
from statistics import fmean, pstdev

import networkx as nx
from bhv.lookup import StoreList
# from bhv.np import NumPyPacked64BHV as BHV
from bhv.native import NativePackedBHV as BHV
from random import shuffle


def score_undirected_nbs(g: nx.Graph, nbsf):
    counts = []
    overs = []
    unders = []

    for n in g.nodes:
        truth = set(g.neighbors(n))
        predicted = set(nbsf(n))
        count = len(truth)
        over = len(predicted - truth)
        under = len(truth - predicted)
        counts.append(count)
        overs.append(over)
        unders.append(under)
    return counts, overs, unders


def convert(g: nx.Graph, k=100, s_power=6):
    hvs = {n: BHV.rand() for n in g.nodes}
    edges = list(g.edges)

    for _ in range(k):
        for x, y in edges:
            hvx = hvs[x]
            hvy = hvs[y]

            c = hvx.select_rand(hvy)

            hvx_ = c.select_rand2(hvx, s_power)
            hvy_ = c.select_rand2(hvy, s_power)

            hvs[x] = hvx_
            hvs[y] = hvy_

        shuffle(edges)
    return hvs


conversion_times = []
scoring_times = []
avg_overshoot = []
avg_undershoot = []

for i in range(5):
    print("repetition", i)
    G = nx.erdos_renyi_graph(1000, 0.03)
    t0 = monotonic()
    hvs = convert(G, k=100)
    ct = monotonic() - t0
    print("conversion time:", ct)
    conversion_times.append(ct)

    store = StoreList(hvs)

    t0 = monotonic()
    cs, os, us = score_undirected_nbs(G, lambda n: store.related(hvs[n], threshold=4.2))
    st = monotonic() - t0
    print("scoring time:", st)
    scoring_times.append(st)
    mcs = fmean(cs)
    print("stats:", mcs, "+-", pstdev(cs))
    mos = fmean(os)
    mus = fmean(us)
    print("overshoot:", mos, "undershoot", mus)
    avg_overshoot.append(mos/mcs)
    avg_undershoot.append(mus/mcs)


print("conversion time:", fmean(conversion_times), "+-", pstdev(conversion_times))
print("scoring time:", fmean(scoring_times), "+-", pstdev(scoring_times))
print("overshoot loss:", fmean(avg_overshoot), "+-", pstdev(avg_overshoot))
print("undershoot loss:", fmean(avg_undershoot), "+-", pstdev(avg_undershoot))


"""
Adam Workstation
conversion time: 36.76595135960088 +- 2.7012157469967595
scoring time: 1.2474143017985626 +- 0.1966217042303927
overshoot loss: 0.4233308465687486 +- 0.017857351877257684
undershoot loss: 0.23999347992728137 +- 0.005390150353930838

AWS m7i.large
conversion time: 21.835669670000062 +- 0.19946246513497012
scoring time: 0.9246955677999722 +- 0.005609435524958635
overshoot loss: 0.033381120159693314 +- 0.00018716759180082814
undershoot loss: 1.0 +- 0.0

Azure HBv4
conversion time: 21.16814346480005 +- 0.4827642068793464
scoring time: 1.0544608715998947 +- 0.009555677903354964
overshoot loss: 0.03343680293649798 +- 0.00036683930977169846
undershoot loss: 1.0 +- 0.0

"""
