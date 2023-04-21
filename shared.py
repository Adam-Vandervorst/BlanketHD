import matplotlib.pyplot as plt


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
