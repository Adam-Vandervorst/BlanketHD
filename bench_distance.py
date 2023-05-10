from time import monotonic
from statistics import fmean, pstdev

import networkx as nx
from bhv.np import NumPyPacked64BHV as BHV


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

    for i in range(k):
        for x, y in g.edges:
            hvx = hvs[x]
            hvy = hvs[y]

            if hvx.bit_error_rate(hvy) > .5 - p:
                c = hvx.select_rand(hvy)

                hvx_ = c.select_rand2(hvx, s_power)
                hvy_ = c.select_rand2(hvy, s_power)

                hvs[x] = hvx_
                hvs[y] = hvy_
    return hvs


G = nx.erdos_renyi_graph(1000, 0.03)
P = 0.05
t0 = monotonic()
hvs = convert(G, p=P)
print("conversion time:", monotonic() - t0)


t0 = monotonic()
cs, os, us = score_undirected_nbs(G, lambda n: (n_ for n_ in G.nodes if n != n_ and not hvs[n_].unrelated(hvs[n], 6.5)))
print("scoring time:", monotonic() - t0)
print("stats:", fmean(cs), pstdev(cs))
print("scores:", fmean(os), fmean(us))
