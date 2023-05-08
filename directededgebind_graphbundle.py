from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt


def convert(g: nx.Graph):
    hvs = {n: BHV.rand() for n in g.nodes}
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y].permute(1))

    return hvs, BHV.majority(binds)


G = nx.erdos_renyi_graph(100, 0.05, directed=True)

hvs, Ghv = convert(G)

for n in G.nodes:
    print(n)
    print(sorted(G.adj[n].keys()))
    hv = hvs[n]
    nbs = (Ghv ^ hv).permute(-1)
    print(sorted([n_ for n_ in G.nodes if not hvs[n_].unrelated(nbs, 3)]))
