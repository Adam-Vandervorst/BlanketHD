import matplotlib.pyplot as plt
from statistics import fmean, pstdev


def compare_adjs(adj, sim, labels):
    N = len(adj)
    assert N == len(adj[0]) == len(sim) == len(sim[0]) == len(labels)
    fig, (ax_adj, ax_sim) = plt.subplots(1, 2)
    ax_adj.set_xticks(range(N))
    ax_adj.set_xticklabels(labels)
    ax_adj.set_yticks(range(N))
    ax_adj.set_yticklabels(labels)
    ax_adj.matshow(adj)
    ax_sim.set_xticks(range(N))
    ax_sim.set_xticklabels(labels)
    ax_sim.set_yticks(range(N))
    ax_sim.set_yticklabels(labels)
    ax_sim.matshow(sim)
    plt.show()


def calc_nbs(g, nbsf):
    counts = []
    overs = []
    unders = []

    for n in g.nodes:
        truth = set(g.neighbors(n))

        predicted = set(nbsf(n))

        count = len(truth)
        over = len(predicted - truth)
        under = len(truth - predicted)

        counts.append(count)
        overs.append(over)
        unders.append(under)
    return counts, overs, unders


def score_nbs(g, nbsf):
    cs, os, us = calc_nbs(g, nbsf)
    print("mean edges", fmean(cs), "std edges", pstdev(cs))
    print("mean edge overshoot", fmean(os), "mean edge undershoot", fmean(us))
