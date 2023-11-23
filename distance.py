from bhv.native import NativePackedBHV as BHV

import networkx as nx
import matplotlib.pyplot as plt
from random import choices

from shared import score_nbs


def convert(g: nx.Graph, initial=None, p=0.05, k=100, s=1/2**6):
    hvs = initial or BHV.nrand(len(g.nodes))

    for i in range(k):
        for x, y in g.edges:
            hvx = hvs[x]
            hvy = hvs[y]

            if hvx.bit_error_rate(hvy) > .5 - p:
                c = hvx.select_rand(hvy)

                hvx_ = c.select_random(hvx, s)
                hvy_ = c.select_random(hvy, s)

                hvs[x] = hvx_
                hvs[y] = hvy_
    return hvs


G = nx.karate_club_graph()
P = 4
hvs = convert(G, p=BHV.std_to_frac(P))

score_nbs(G, lambda n: hvs[n].within_std(hvs, -4, relative=True), include_diag=True)
