from random import random

import networkx as nx
import matplotlib.pyplot as plt
from bhv.native import NativePackedBHV as BHV

from shared import score_nbs


def convert(g: nx.DiGraph, initial=None, m=.5):
    hvs = initial or BHV.nrand(len(g.nodes))

    return [BHV.random(m).select(hvs[x], BHV.majority([
                hvs[y] for y in g.adj[x].keys()
            ])) for x in g.nodes]


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

hvs = convert(G)

score_nbs(G, lambda n: hvs[n].within_std(hvs, -7, True), include_diag=True)
