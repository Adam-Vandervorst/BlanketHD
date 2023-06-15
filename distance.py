from bhv.lookup import StoreList
from bhv.np import NumPyPacked64BHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import choices

from shared import score_nbs


def convert(g: nx.Graph, initial=None, p=0.05, k=100, s_power=6):
    hvs = initial or {n: BHV.rand() for n in g.nodes}

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
P = 4
hvs = convert(G, p=BHV.std_to_frac(P))

store = StoreList(hvs)
score_nbs(G, lambda n: store.related(hvs[n], threshold=4), include_diag=True)
