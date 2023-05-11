from random import random

import networkx as nx
import matplotlib.pyplot as plt
from bhv.np import NumPyPacked64BHV as BHV

from shared import score_nbs


def convert(g: nx.DiGraph, initial=None):
    if initial is None:
        initial = {n: BHV.rand() for n in g.nodes}

    return {x: initial[x].select_rand(BHV.majority([
                initial[y] for y in g.adj[x].keys()
            ])) for x in g.nodes}


G = nx.erdos_renyi_graph(50, 0.05, directed=True)

hvs = convert(G)

score_nbs(G, lambda n: (n_ for n_ in G.nodes if n != n_ and not hvs[n].unrelated(hvs[n_], 8)))
