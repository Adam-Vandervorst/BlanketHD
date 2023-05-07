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
    hv = hvs[n]
    print(sorted(G.adj[n].keys()))
    nbs = Ghv ^ hv
    print(sorted([n for n in G.nodes if not hvs[n].unrelated(nbs)]))
