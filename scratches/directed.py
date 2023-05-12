from bhv.np import NumPyBoolBHV as BHV

#     ^    F L
# c < c3    γ
#   L v
# c1  c2


u1, u2 = BHV.nrand(2)
p = 1/4
R = BHV.random(p)
def lr(l, r): return l.bias_rel(r, R)

print(u1.active_fraction(), u2.active_fraction())
print(lr(u1, u2), lr(u2, u1))
print(u1.bit_error_rate(u2))

u1_ = R.select(u1.flip_frac_on((1-p)/2), u1.flip_frac_off(p/2))
u2_ = R.select(u2.flip_frac_off((1-p)/2), u2.flip_frac_on(p/2))
print()

print(u1_.active_fraction(), u2_.active_fraction())
print(lr(u1_, u2_), lr(u2_, u1_))
print(u2_.bit_error_rate(u1_))
