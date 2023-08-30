from bhv.np import NumPyPacked64BHV as BHV
from bhv.lookup import StoreList

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
    #  {x ^ x ^ y, x ^ x ^ z, x ^ y ^ q}
    #  {y, z, x ^ y ^ q}
    #  {y, z}

    return hvs, BHV.majority(binds)


G = nx.karate_club_graph()

hvs, Ghv = convert(G)

store = StoreList(hvs)
score_nbs(G, lambda n: store.related(hvs[n] ^ Ghv))
