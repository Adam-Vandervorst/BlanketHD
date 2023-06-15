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
Adam Workstation  (OUTDATED)
conversion time: 64.92264482758473 +- 1.3443107052971761
scoring time: 4.556829810584896 +- 0.05932598371485799
overshoot loss: 0.17745430970212372 +- 0.04014832701293576
undershoot loss: 0.360622835307186 +- 0.026702056348248782

Adam Laptop
conversion time: 15.978824611399613 +- 0.0712963626382589
scoring time: 0.8618214570000419 +- 0.0051379973708396065
overshoot loss: 0.43790523390560976 +- 0.022149696414124755
undershoot loss: 0.23963386756434352 +- 0.010714618122068262

AWS c6i.large  (OUTDATED)
conversion time: 57.702627090600004 +- 0.5105765311043634
scoring time: 8.311138239999991 +- 0.06991942551272408
overshoot loss: 0.16692675233013826 +- 0.03326871875573161
undershoot loss: 0.36863357440624983 +- 0.030591340731719513
"""
