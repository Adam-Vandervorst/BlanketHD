from time import monotonic
from statistics import fmean, pstdev

import networkx as nx
from bhv.np import NumPyPacked64BHV as BHV
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


def convert(g: nx.Graph, p=0.05, k=100, s_power=6):
    hvs = {n: BHV.rand() for n in g.nodes}
    edges = list(g.edges)

    for _ in range(k):
        for x, y in edges:
            hvx = hvs[x]
            hvy = hvs[y]

            if hvx.bit_error_rate(hvy) > .5 - p:
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
    P = 0.05
    t0 = monotonic()
    hvs = convert(G, p=P)
    ct = monotonic() - t0
    print("conversion time:", ct)
    conversion_times.append(ct)

    t0 = monotonic()
    cs, os, us = score_undirected_nbs(G, lambda n: (n_ for n_ in G.nodes if n != n_ and not hvs[n_].unrelated(hvs[n], 6.5)))
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
Workstation, 5 repetitions
conversion time: 64.92264482758473 +- 1.3443107052971761
scoring time: 4.556829810584896 +- 0.05932598371485799
overshoot loss: 0.17745430970212372 +- 0.04014832701293576
undershoot loss: 0.360622835307186 +- 0.026702056348248782
"""
