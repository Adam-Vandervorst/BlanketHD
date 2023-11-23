from bhv.native import NativePackedBHV as BHV

import networkx as nx
import matplotlib.pyplot as plt

from shared import score_nbs


def convert(g: nx.Graph, initial=None):
    hvs = initial or BHV.nrand(len(g.nodes))
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

score_nbs(G, lambda n: (hvs[n] ^ Ghv).within_std(hvs, -4, relative=True))
