from bhv.np import NumPyBoolBHV as BHV


#   R  S
#   |/
# A----B

A, B, R, S = BHV.nrand(4)
pow = 1
def test(s, p, o): return s.bias_rel(o, p)

print(A.active_fraction(), B.active_fraction())
print(test(A, B, R), test(B, A, R))
print(A.bit_error_rate(B))


def bias_ps(s, ps, o):
    mps = BHV.majority(ps)
    s_ = mps.select(s.flip_pow_on(pow), s.flip_pow_off(pow))
    o_ = mps.select(o.flip_pow_off(pow), o.flip_pow_on(pow))
    return s_, o_

def bias_p(s, p, o):
    s_ = p.select(s.flip_pow_on(pow), s.flip_pow_off(pow))
    o_ = p.select(o.flip_pow_off(pow), o.flip_pow_on(pow))
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


"""
0.4918212890625 0.501708984375
0.4943932220284077 0.5026602482898404
0.5091552734375

0.4915771484375 0.503173828125
0.5496754867698452 0.45032451323015477
0.5556633519282076 0.4443366480717924
0.5179443359375
"""
