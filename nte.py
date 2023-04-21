from bhv.np import NumPyBoolBHV as BHV


#   R  S
#   |/
# A----B

A, B, R, S = BHV.nrand(4)
frac = 1/4
def test(s, p, o): return s.bias_rel(o, p)

print(A.active_fraction(), B.active_fraction())
print(test(A, B, R), test(B, A, R))
print(A.bit_error_rate(B))


def bias_ps(s, ps, o):
    s_ = BHV.majority(ps).select(s.mix(BHV.ONE, 1 - frac), BHV.ZERO.mix(s, frac))
    o_ = BHV.majority(ps).select(o.mix(BHV.ZERO, 1 - frac), BHV.ONE.mix(o, frac))
    return s_, o_

def bias_p(s, p, o):
    s_ = p.select(s.mix(BHV.ONE, 1 - frac), BHV.ZERO.mix(s, frac))
    o_ = p.select(o.mix(BHV.ZERO, 1 - frac), BHV.ONE.mix(o, frac))
    return s_, o_

def _bias_ps_via_bias_p(s, ps, o):
    ss, os = zip(*[bias_p(s, p, o) for p in ps])
    return BHV.majority(ss), BHV.majority(os)


A_, B_ = bias_ps(A, [R, S], B)

print()

print(A_.active_fraction(), B_.active_fraction())
print(test(A_, R, B_), test(B_, R, A_))
print(test(A_, S, B_), test(B_, S, A_))
print(A_.bit_error_rate(B_))
