from random import random

import networkx as nx
import matplotlib.pyplot as plt
from bhv.np import NumPyPacked64BHV as BHV

from shared import score_nbs


def convert(g: nx.DiGraph, initial=None):
    hvs = initial or {n: BHV.rand() for n in g.nodes}

    return {x: hvs[x].select_rand(BHV.majority([
                hvs[y] for y in g.adj[x].keys()
            ])) for x in g.nodes}


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

hvs = convert(G)

score_nbs(G, lambda n: (n_ for n_ in G.nodes if n != n_ and not hvs[n].unrelated(hvs[n_], 8)))
