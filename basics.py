import torch
import torchhd
import matplotlib.pyplot as plt


d = 8192
# d = 10_000_000


def flip_frac(original, frac_change):
    return torchhd.randsel(original, torchhd.random(1, d)[0], p=(1 - frac_change))


def bit_error_rate(input, others):
    return torchhd.hamming_similarity(input, others)/d


def flip_frac_to_bit_error_rate(frac_change):
    return frac_change/2 + 0.5


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

root1, root2 = torchhd.random(2, d)
# distance one-step nodes
p = 0.2
# approx. distance of intermediate-step nodes
ph = p**.5
# approx. distance of two-step nodes
ps = p**2
# approx. distance of three-step nodes
pss = p**3
print(p, ph, ps, pss)

a = root1
b = flip_frac(root1, p)
c = flip_frac(root1, p)
c1 = flip_frac(c, p)
c2 = flip_frac(c, p)
c3 = flip_frac(c, p)
α = flip_frac(root2, ph)
β = flip_frac(root2, ph)
γ = flip_frac(root2, ph)


ns = torch.stack([a, b, c, c1, c2, c3, α, β, γ])

sim = bit_error_rate(ns, ns)
assert bit_error_rate(a, b) == sim[0, 1] and bit_error_rate(β, γ) == sim[-1, -2]

print(bit_error_rate_to_flip_frac(bit_error_rate(a, b).item()),
      bit_error_rate_to_flip_frac(bit_error_rate(root2, α).item()),
      bit_error_rate_to_flip_frac(bit_error_rate(a, c1).item()),
      bit_error_rate_to_flip_frac(bit_error_rate(b, c1).item()),
      bit_error_rate_to_flip_frac(bit_error_rate(b, β).item()))

plt.matshow(sim - torch.diag(torch.full((len(sim),), .5)))
plt.matshow(adj)
plt.show()
