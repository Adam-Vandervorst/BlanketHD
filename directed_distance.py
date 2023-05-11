from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import random, choice

from shared import score_undirected_nbs


R = BHV.rand()
def lr(l, r): return l.bias_rel(r, R ^ l)


def convert(g: nx.DiGraph, p=0.05, k=1000, s_power=5, r_power=8):
    hvs = {n: BHV.rand() for n in g.nodes}
    edges = list(g.edges)

    for i in range(k*len(edges)):
        (x, y) = choice(edges)
        hvx = hvs[x]
        hvy = hvs[y]

        lrxy = lr(hvx, hvy)
        # print(lrxy)
        to_flip = lrxy - (.5 - p)

        if to_flip > 0:
            e = 0.0001
            hvy_ = (R ^ hvx).select(hvy | hvy.flip_frac(to_flip + e), hvy & hvy.flip_frac(to_flip + e))
            # print(lr(hvx, hvy_), hvx.active_fraction(), hvy_.active_fraction())
            hvs[y] = hvy_
    return hvs


G_ = nx.erdos_renyi_graph(100, 0.1)
G = nx.DiGraph()
for (x, y) in G_.edges:
    G.add_edge(x, y)

P = .03
hvs = convert(G, p=P)

score_undirected_nbs(G, lambda n: [n_ for n_ in G.nodes if lr(hvs[n], hvs[n_]) < (.5 - P)])
