import torch
import torchhd


D = 8192
# D = 10_000_000


a, b, c = torchhd.random(3, D, "BSC")

a_or_b = torch.bitwise_or(a, b)
b_or_c = torch.bitwise_or(b, c)
a_or_c = torch.bitwise_or(a, c)

a_or_b_or_c = torch.bitwise_or(torch.bitwise_or(a, b), c)

assert torch.all(torch.less_equal(a, a_or_b)).item()
assert not torch.all(torch.less_equal(a, b_or_c)).item()
assert torch.all(torch.less_equal(b_or_c, a_or_b_or_c))
