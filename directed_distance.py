from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import random, choice

from shared import score_nbs


R = BHV.rand()
def lr(l, r): return l.bias_rel(r, R ^ l)


def convert(g: nx.DiGraph, initial=None, p=0.02, k=100, s_power=4):
    hvs = initial or {n: BHV.rand() for n in g.nodes}
    edges = list(g.edges)

    for i in range(k*len(edges)):
        (x, y) = choice(edges)
        hvx, hvy = hvs[x], hvs[y]
        lrxy = lr(hvx, hvy)

        if lrxy > (.5 - p):
            hvs[y] = (R ^ hvx).select_rand2(hvy, s_power)
    return hvs


G_ = nx.erdos_renyi_graph(100, 0.1)
G = nx.DiGraph()
for (x, y) in G_.edges:
    G.add_edge(x, y)

P = .02
hvs = convert(G, p=P)

score_nbs(G, lambda n: [n_ for n_ in G.nodes if lr(hvs[n], hvs[n_]) < (.5 - P)])
