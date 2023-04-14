from bhv.np import NumPyBoolBHV as BHV
import matplotlib.pyplot as plt


def bit_error_rate_to_flip_frac(ber):
    return ber*2 - 1

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
p = 0.2
# approx. distance of intermediate-step nodes
ph = p/2
print(p, ph, ps, pss)

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

sim = [[.5 if x == y else 1 - x.bit_error_rate(y) for x in ns] for y in ns]

print(a.bit_error_rate(b),
      root2.bit_error_rate(α),
      a.bit_error_rate(c1),
      b.bit_error_rate(c1),
      b.bit_error_rate(β),
      α.bit_error_rate(β))

plt.matshow(sim)
plt.matshow(adj)
plt.show()
