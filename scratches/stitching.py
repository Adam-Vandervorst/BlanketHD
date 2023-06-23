from bhv.np import NumPyBoolBHV as BHV
import matplotlib.pyplot as plt

#  a - b   α - β
#  | / |
#  c - d
adj = [
#    a  b  c  d  α  β
    [0, 1, 1, 0, 0, 0],  # a
    [1, 0, 1, 1, 0, 0],  # b
    [1, 1, 0, 1, 0, 0],  # c
    [0, 1, 1, 0, 0, 0],  # d

    [0, 0, 0, 0, 0, 1],  # α
    [0, 0, 0, 0, 1, 0],  # β
]

root1_a, root1_b, root2 = BHV.nrand(3)
# distance one-step nodes
p = 1/3
# approx. distance of intermediate-step nodes
ph = 1/9

a = root1_a.flip_frac(ph)
b = root1_a.flip_frac(ph).mix(root1_b.flip_frac(ph))
c = root1_a.flip_frac(ph).mix(root1_b.flip_frac(ph))
d = root1_b.flip_frac(ph)

α = root2
β = root2.flip_frac(p)


ns = [a, b, c, d, α, β]

sim = [[.5 if x == y else 1. - x.bit_error_rate(y) for x in ns] for y in ns]

print(a.bit_error_rate(b),
      a.bit_error_rate(d),
      b.bit_error_rate(β),
      α.bit_error_rate(β))

ls = ["", "a", "b", "c", "d", "α", "β"]
fig, (ax_adj, ax_sim) = plt.subplots(1, 2)
ax_adj.set_xticklabels(ls)
ax_adj.set_yticklabels(ls)
ax_adj.matshow(adj)
ax_sim.set_xticklabels(ls)
ax_sim.set_yticklabels(ls)
ax_sim.matshow(sim)
plt.show()
