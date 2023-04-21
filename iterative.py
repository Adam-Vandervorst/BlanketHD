from random import randrange
from bhv.np import NumPyBoolBHV as BHV
from shared import compare_adjs


# a - b   α - β
# |        \ /
# c- c3     γ
# |\
# c1 c2
adj = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0],  # a
    [1, 0, 0, 0, 0, 0, 0, 0, 0],  # b
    [1, 0, 0, 1, 1, 1, 0, 0, 0],  # c

    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # c1
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # c2
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # c3

    [0, 0, 0, 0, 0, 0, 0, 1, 1],  # α
    [0, 0, 0, 0, 0, 0, 1, 0, 1],  # β
    [0, 0, 0, 0, 0, 0, 1, 1, 0],  # γ
]
N = len(adj)

p = 0.1

ns = BHV.nrand(N)

for epoch in range(1000):
    i = randrange(0, N)
    j = randrange(0, N)

    if adj[i][j]:
        ni = ns[i]
        nj = ns[j]

        if ni.bit_error_rate(nj) > .5 - p:
            c = ni.select_rand(nj)

            ni_ = c.select_rand2(ni, 6)
            nj_ = c.select_rand2(nj, 6)

            ns[i] = ni_
            ns[j] = nj_


a, b, c, c1, c2, c3, α, β, γ = ns

sim = [[0 if x == y else x.std_apart(y, invert=True) for x in ns] for y in ns]

print(a.bit_error_rate(b),
      a.bit_error_rate(c1),
      b.bit_error_rate(c1),
      b.bit_error_rate(β),
      α.bit_error_rate(β))


ls = ["a", "b", "c", "c1", "c2", "c3", "α", "β", "γ"]

compare_adjs(adj, sim, ls)
