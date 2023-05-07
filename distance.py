from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import choices


def convert(g: nx.Graph, p=0.05, k=100, s_power=6):
    hvs = {n: BHV.rand() for n in g.nodes}

    for i in range(k):
        for x, y in g.edges:
            hvx = hvs[x]
            hvy = hvs[y]

            if hvx.bit_error_rate(hvy) > .5 - p:
                c = hvx.select_rand(hvy)

                hvx_ = c.select_rand2(hvx, s_power)
                hvy_ = c.select_rand2(hvy, s_power)

                hvs[x] = hvx_
                hvs[y] = hvy_
    return hvs


G = nx.karate_club_graph()
P = 0.05
hvs = convert(G, p=P)

for n in G.nodes:
    print(n)
    print(sorted(G.adj[n].keys()))
    hv = hvs[n]
    print(sorted([n_ for n_ in G.nodes if n != n_ and hvs[n_].bit_error_rate(hv) < .5 - P]))
