from time import monotonic
from statistics import fmean, pstdev
from random import sample
from multiprocessing import Pool


import networkx as nx
# from bhv.np import NumPyPacked64BHV as BHV
from bhv.np import NumPyBoolBHV as BHV


def score_undirected_nbs(g: nx.Graph, nbsf, check_frac=.1):
    counts = []
    overs = []
    unders = []
    to_check = sample(list(g.nodes), int(len(g)*check_frac))

    with Pool() as p:
        results = p.map(nbsf, to_check)

    for n, result in zip(to_check, results):
        truth = set(g.neighbors(n))
        predicted = set(result)
        count = len(truth)
        over = len(predicted - truth)
        under = len(truth - predicted)
        counts.append(count)
        overs.append(over)
        unders.append(under)
    return counts, overs, unders


def convert(g: nx.Graph, initial=None, ms=10, red=2):
    hvs = initial or {n: BHV.rand() for n in g.nodes}
    binds = []

    for x, y in g.edges:
        binds.append(hvs[x] ^ hvs[y])

    E = len(binds)
    blankets = []
    for _ in range(ms):
        ss = sample(binds, int(red*E/ms))
        blankets.append(BHV.majority(ss))

    return hvs, blankets


conversion_times = []
scoring_times = []
avg_overshoot = []
avg_undershoot = []

for i in range(5):
    print("repetition", i)
    G = nx.erdos_renyi_graph(1000, 0.03)
    t0 = monotonic()
    RED = 2
    B = 1000//(30//RED)
    hvs, blankets = convert(G, ms=B, red=RED)
    ct = monotonic() - t0
    print("conversion time:", ct)
    conversion_times.append(ct)

    def nbs(n):
        hv = hvs[n]
        nbs_options = [blanket ^ hv for blanket in blankets]
        return [n_ for n_ in G.nodes if
                sum(not hvs[n_].unrelated(nbs_option, 3) for nbs_option in nbs_options) >= RED]


    t0 = monotonic()
    cs, os, us = score_undirected_nbs(G, nbs)
    st = monotonic() - t0
    print("scoring time:", st)
    scoring_times.append(st)
    mcs = fmean(cs)
    print("stats:", mcs, pstdev(cs))
    mos = fmean(os)
    mus = fmean(us)
    print("scores:", mos, mus)
    avg_overshoot.append(mos/mcs)
    avg_undershoot.append(mus/mcs)


print("conversion time:", fmean(conversion_times), "+-", pstdev(conversion_times))
print("scoring time:", fmean(scoring_times), "+-", pstdev(scoring_times))
print("overshoot loss:", fmean(avg_overshoot), "+-", pstdev(avg_overshoot))
print("undershoot loss:", fmean(avg_undershoot), "+-", pstdev(avg_undershoot))


"""
Workstation 8 cores
5 repetitions

100 nodes
1000 nodes
1 "blanket"
conversion time: 0.41756714361254127 +- 0.0639423438148542
scoring time: 18.3407090557972 +- 0.3667289361444694
overshoot loss: 1.4830413311629933 +- 0.01862748160240708
undershoot loss: 0.9156151054085824 +- 0.0008664566438166838

10 disjoint blankets
conversion time: 0.27036310725379736 +- 0.08165714798055752
scoring time: 19.453217881778254 +- 1.5002943874405423
overshoot loss: 0.8660483205272256 +- 0.004537876946644023
undershoot loss: 0.8584963204797453 +- 0.0018336164642588188

1000/15 redundancy 2 blankets (checking 1 in 10)
conversion time: 0.29750877760816363 +- 0.023177128075548694
scoring time: 14.277609395817853 +- 0.33073695574466166
overshoot loss: 0.48151527113324183 +- 0.01243587218646209
undershoot loss: 0.5596952976672627 +- 0.006146080351486295
"""
