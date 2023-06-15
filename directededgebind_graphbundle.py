from bhv.lookup import StoreList
from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt

from shared import score_nbs


def convert(g: nx.DiGraph, initial=None):
    hvs = initial or {n: BHV.rand() for n in g.nodes}
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y].permute(1))

    return hvs, BHV.majority(binds)


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

P = 3
hvs, Ghv = convert(G)


store = StoreList(hvs)
score_nbs(G, lambda n: store.related((Ghv ^ hvs[n]).permute(-1), P))
