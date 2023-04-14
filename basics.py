from bhv.np import NumPyBoolBHV as BHV
import matplotlib.pyplot as plt


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

root1, root2 = BHV.nrand(2)
# distance one-step nodes
p = 0.1
# approx. distance of intermediate-step nodes
ph = 0.05

a = root1
b = root1.flip_frac(p)
c = root1.flip_frac(p)
c1 = c.flip_frac(p)
c2 = c.flip_frac(p)
c3 = c.flip_frac(p)
α = root2.flip_frac(ph)
β = root2.flip_frac(ph)
γ = root2.flip_frac(ph)


ns = [a, b, c, c1, c2, c3, α, β, γ]

sim = [[0 if x == y else x.std_apart(y, invert=True) for x in ns] for y in ns]

print(a.bit_error_rate(b),
      root2.bit_error_rate(α),
      a.bit_error_rate(c1),
      b.bit_error_rate(c1),
      b.bit_error_rate(β),
      α.bit_error_rate(β))

ls = ["", "a", "b", "c", "c1", "c2", "c3", "α", "β", "γ"]
fig, (ax_adj, ax_sim) = plt.subplots(1, 2)
ax_adj.set_xticklabels(ls)
ax_adj.set_yticklabels(ls)
ax_adj.matshow(adj)
ax_sim.set_xticklabels(ls)
ax_sim.set_yticklabels(ls)
ax_sim.matshow(sim)
plt.show()
