from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt

from shared import score_nbs


def convert(g: nx.Graph, initial=None):
    hvs = initial or {n: BHV.rand() for n in g.nodes}
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y])

    #  x - y - q
    #  |
    #  z
    #
    #  Ghv = {x ^ y, x ^ z, y ^ q}
    #
    #  nbs(x)
    #  x ^ Ghv
    #  x ^ {x ^ y, x ^ z, y ^ q}
    #  {x ^ x ^ y, x ^ x ^ z, y ^ q}
    #  {y, z, y ^ q}
    #  {y, z}

    return hvs, BHV.majority(binds)


G = nx.karate_club_graph()

hvs, Ghv = convert(G)


def nbs(n):
    hv = hvs[n]
    nbs = Ghv ^ hv
    return [n_ for n_ in G.nodes if not hvs[n_].unrelated(nbs)]


score_nbs(G, nbs)
