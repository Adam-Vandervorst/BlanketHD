from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import random


R = BHV.rand()
def lr(l, r): return l.bias_rel(r, R ^ l)


def convert(g: nx.DiGraph, initial=None):
    if initial is None:
        initial = {n: BHV.rand() for n in g.nodes}

    return {x: initial[x].select_rand(BHV.majority([
                initial[y] for y in g.adj[x].keys()
            ])) for x in g.nodes}


G = nx.erdos_renyi_graph(100, 0.05, directed=True)

hvs = convert(G)

for n in G.nodes:
    print(n)
    print(sorted(G.adj[n].keys()))
    hv = hvs[n]
    print(sorted([n_ for n_ in G.nodes if n != n_ and not hv.unrelated(hvs[n_], 8)]))
