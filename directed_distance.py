from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import random


R = BHV.rand()
def lr(l, r): return l.bias_rel(r, R ^ l)


def convert(g: nx.DiGraph, p=0.05, k=2000, s_power=6):
    hvs = {n: BHV.rand() for n in g.nodes}
    edges = set(g.edges)

    for i in range(k):
        # TODO clean up
        for x in g.nodes:
            for y in g.nodes:
                hvx = hvs[x]
                hvy = hvs[y]

                if (x, y) in edges:
                    d = .49
                    print(x, y, lr(hvx, hvy))
                    if lr(hvx, hvy) < .5 + p:
                        hvx_ = (R ^ hvx).select(hvx | hvx.flip_frac_off(d), hvx & hvx.flip_frac_on(d))
                        hvy_ = (R ^ hvx).select(hvy & hvx.flip_frac_on(d), hvy | hvx.flip_frac_off(d))
                        print(lr(hvx_, hvy_))
                        hvs[x] = hvx_
                        hvs[y] = hvy_
                elif i < 1500:
                    hvs[x] = hvx.randomize_pow(9)
                    hvs[y] = hvy.randomize_pow(9)
    return hvs


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

hvs = convert(G)

for n in G.nodes:
    print(n)
    print(sorted(G.adj[n].keys()))
    hv = hvs[n]
    print(sorted([n_ for n_ in G.nodes if lr(hv, hvs[n_]) > .55]))
