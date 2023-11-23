from time import monotonic
from statistics import fmean, pstdev
from random import sample
from multiprocessing import Pool


import networkx as nx
# from bhv.np import NumPyPacked64BHV as BHV
from bhv.native import NativePackedBHV as BHV


#  nbsf has type nx.Node -> [nx.Node]
#  and the oracle satisfying this is g.neighbors
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


def convert(g: nx.Graph, initial=None, nblankets=10, redundancy=2):
    hvs = initial or {n: BHV.rand() for n in g.nodes}

    with Pool() as p:
        binds = p.starmap(BHV.__xor__, [(hvs[x], hvs[y]) for x, y in g.edges])
        blankets = p.map(BHV.majority, [sample(binds, int(redundancy*len(binds)/nblankets)) for _ in range(nblankets)])
    return hvs, blankets


N = 1000
Ef = 0.03
RED = 2
B = N//(30//RED)  # 30 is the capacity of a majority bundle used


conversion_times = []
scoring_times = []
avg_overshoot = []
avg_undershoot = []

for i in range(5):
    print("repetition", i)
    G = nx.erdos_renyi_graph(N, Ef)
    t0 = monotonic()
    hvs, blankets = convert(G, nblankets=B, redundancy=RED)
    ct = monotonic() - t0
    print("conversion time:", ct)
    conversion_times.append(ct)

    def nbs(n):
        hv = hvs[n]
        nbs_options = [blanket ^ hv for blanket in blankets]
        return [n_ for n_ in G.nodes if
                sum(hvs[n_].related(nbs_option, 3) for nbs_option in nbs_options) >= RED]


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
Adam Workstation
conversion time: 0.2788123039994389 +- 0.042903326702766705
scoring time: 1.1538768206024543 +- 0.011007476261102168
overshoot loss: 0.492798784924418 +- 0.03098208082093101
undershoot loss: 0.5600437279433577 +- 0.009693142355089087

Azure HBv4
conversion time: 0.32892023340000376 +- 0.013533457504777626
scoring time: 0.35380649539984005 +- 0.012133735484164201
overshoot loss: 0.48203651044844414 +- 0.014193690606825547
undershoot loss: 0.563029737032123 +- 0.005069288395927521

"""
