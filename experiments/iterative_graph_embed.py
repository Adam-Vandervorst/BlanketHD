from bhv.native import NativePackedBHV as BHV

import networkx as nx
import optuna
from datetime import timedelta

from statistics import fmean, pstdev
import itertools


def calc_nbs(g, nbsf, include_diag=False):
    counts = []
    overs = []
    unders = []

    for n in g.nodes:
        truth = set(g.neighbors(n))

        if include_diag is not None:
            if include_diag: truth.add(n)
            elif n in truth: truth.remove(n)

        predicted = set(nbsf(n))

        count = len(truth)
        over = len(predicted - truth)
        under = len(truth - predicted)

        counts.append(count)
        overs.append(over)
        unders.append(under)
    return counts, overs, unders


def score_nbs(g, nbsf, include_diag=False):
    cs, os, us = calc_nbs(g, nbsf, include_diag=include_diag)
    # print("mean edges", fmean(cs), "std edges", pstdev(cs))
    # print("mean edge overshoot", fmean(os), "mean edge undershoot", fmean(us))
    return [fmean(os), fmean(us)]


def convert(g: nx.Graph, initial=None, method='edge', p=0.05, k=100, s=1/2**6, sn=1/2**5, normalize_first=.9):
    assert method in ('edge', 'node', 'clique')
    if method == 'clique':
        cliques = list(nx.find_cliques(g))
        inverse_cnt = {n: [i for i, c in enumerate(cliques) if n in c] for n in g.nodes}
    hvs = initial or BHV.nrand(len(g.nodes))

    for i in range(k):
        if method == 'edge':
            for x, y in g.edges:
                hvx = hvs[x]
                hvy = hvs[y]

                if hvx.bit_error_rate(hvy) > .5 - p:
                    c = hvx.select_rand(hvy)

                    hvx_ = c.select_random(hvx, s)
                    hvy_ = c.select_random(hvy, s)

                    hvs[x] = hvx_
                    hvs[y] = hvy_
        elif method == 'node':
            for n in g.nodes:
                too_far_hvs = [hvs[nb] for nb in g.neighbors(n) if hvs[n].bit_error_rate(hvs[nb]) > .5 - p]
                if not too_far_hvs: continue
                nbs_hv = BHV.majority(too_far_hvs)
                hvs[n] = nbs_hv.select_random(hvs[n], s*len(too_far_hvs))
        elif method == 'clique':
            q_hvs = [BHV.majority([hvs[x] for x in q]) for q in cliques]

            for n, qs in inverse_cnt.items():
                # "furthest" and "top-k-furthest" methods would be useful here
                not_converged_hvs = [q_hvs[q] for q in qs if max(hvs[n].bit_error_rate(hvs[nb]) for nb in cliques[q]) > .5 - p]
                if not not_converged_hvs: continue
                qs_hv = BHV.majority(not_converged_hvs)
                hvs[n] = qs_hv.select_random(hvs[n], s)

        if i < normalize_first*k:
            for x in g.nodes:
                hvs[x] ^= BHV.random(sn)
    return hvs


def process(trial: 'optuna.Trial'):
    method = trial.suggest_categorical("method", ['edge', 'node', 'clique'])
    P = trial.suggest_float('desired_distance', 1., 6.)
    k = trial.suggest_int('epochs', 1, 1000, log=True)
    s = trial.suggest_float('converge_strength', 1e-8, 1/2, log=True)
    sn = trial.suggest_float('diverge_strength', 1e-8, 1/2, log=True)
    normalize_first = trial.suggest_float('normalize_first', 0., 1.)

    hvs = convert(G, None, method, BHV.std_to_frac(P), k, s, sn, normalize_first)

    return score_nbs(G, lambda n: hvs[n].within_std(hvs, -P, relative=True), include_diag=True)


G = nx.erdos_renyi_graph(10000, .01, seed=42)

study = optuna.load_study(study_name="iterative-graph-2", storage="mysql://root@localhost/paramsearch")

study.optimize(process, n_trials=4, timeout=1000, gc_after_trial=True, n_jobs=1)
