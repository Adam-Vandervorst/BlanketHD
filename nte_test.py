from bhv.np import NumPyBoolBHV as BHV

from hedit_utils import HDict


#   R  S
#   |/
# A----B

ABRS = HDict({
    'data': [{'data': "A", 'id': 0}, {'data': "B", 'id': 1}, {'data': "R", 'id': 2}, {'data': "S", 'id': 3}],
    'conn': [(0, 1), (2, (0, 1)), (3, (0, 1))],
    'mode': "property_graph"
})


def bias_ps(s, ps, o, pw=1):
    mps = BHV.majority(ps)
    s_ = mps.select(s.flip_pow_on(pw), s.flip_pow_off(pw))
    o_ = mps.select(o.flip_pow_off(pw), o.flip_pow_on(pw))
    return s_, o_


def convert(nte: HDict, pw=1):
    hvs = {n['id']: BHV.rand() for n in nte.find_nodes()}

    adj_ps = {}
    for src, tgt in nte['conn']:
        if not isinstance(tgt, tuple) or len(tgt) != 2:
            continue
        p = src
        if tgt in adj_ps:
            adj_ps[tgt].append(p)
        else:
            adj_ps[tgt] = [p]

    for (s, o), ps in adj_ps.items():
        hvs[s], hvs[o] = bias_ps(hvs[s], [hvs[p] for p in ps], hvs[o], pw)

    return hvs


hvs = convert(ABRS, pw=1)

for s, o in ABRS['conn']:
    if not isinstance(o, int):
        continue

    ps = [p for (p, e) in ABRS['conn'] if e == (s, o)]

    print(s, o, ps)
    print([p for p in hvs if p != s and hvs[s].bias_rel(hvs[o], hvs[p]) > .5])
