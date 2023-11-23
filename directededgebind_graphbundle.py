from bhv.native import NativePackedBHV as BHV, DIMENSION

import networkx as nx
import matplotlib.pyplot as plt

from shared import score_nbs


def convert(g: nx.DiGraph, initial=None):
    hvs = initial or BHV.nrand(len(g.nodes))
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y].permute(1))

    return hvs, BHV.majority(binds)


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

P = 3
hvs, Ghv = convert(G)

score_nbs(G, lambda n: (Ghv ^ hvs[n]).permute(-1).within_std(hvs, -4, relative=True))
