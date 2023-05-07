from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt


def convert(g: nx.Graph):
    hvs = {n: BHV.rand() for n in g.nodes}
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y])

    return hvs, BHV.majority(binds)


G = nx.karate_club_graph()

hvs, Ghv = convert(G)

for n in G.nodes:
    print(n)
    print(sorted(G.adj[n].keys()))
    hv = hvs[n]
    nbs = Ghv ^ hv
    print(sorted([n_ for n_ in G.nodes if not hvs[n_].unrelated(nbs)]))
