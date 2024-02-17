from time import monotonic_ns

from bhv.embedding import Random
from bhv.native import NativePackedBHV as BHV


store = [
    (((("L", "1"), "2"), "3"), "4"),
    ("D", ("S", ("S", "Z"))),
    ("D", ("S", ("S", ("S", "Z")))),
    ("P", 0, 0),
    ("X", 0, "Z"),
    ("Y", "Z", 0),
    ("Q1", ("S", ("S", "Z")), ("S", "Z")),
    ("Q2", ("S", "Z"), ("S", ("S", "Z"))),
    ("Q3", "Z", ("S", ("S", ("S", ("S", "Z"))))),
    ("F", ("+", 0, "Z"), -1),
    ("F", ("+", 0, ("S", 0)), ("S", ("+", -1, -2))),
    ("F", ("*", 0, "Z"), "Z"),
    ("F", ("*", 0, ("S", 0)), ("+", -1, ("*", -1, -2))),
]

symbol = Random(BHV)


def paths(term, l, rs, p=()):
    match term:
        case tuple(xs):
            # print("xs", xs)
            return tuple(paths(x, l, rs, p + (1 + i,)) for i, x in enumerate(xs))
        case str(s):
            # print("s", s)
            # l.append((s, p))
            l.append(symbol.forward(s).permute(p))
            return (s, "".join(map(str, p)))
        case 0:
            # print("newvar")
            # rs.append(BHV.rand())
            # l.append((0, p))
            l.append(symbol.forward(0).permute(p))
            return (0, "".join(map(str, p)))
        case int(i):
            # print("ref", i)
            # l.append((i, p))
            l.append(symbol.forward(i).permute(p))
            return (i, "".join(map(str, p)))


def decode(hv, l, p="", mw=4, md=5):
    if len(p) < md:
        for i in range(mw):
            pb = hv.permute(-(i + 1))
            s = symbol.back(pb)
            if s is not None:
                l.append((s, str(i + 1) + p))
            decode(pb, l, str(i + 1) + p, mw, md)


if __name__ == '__main__':
    t0 = monotonic_ns()
    for term in store:
        flat = []
        rs = []
        print("-", paths(term, flat, rs))
        hv = BHV.majority(flat)
        flat_ = []
        decode(hv, flat_)
        print(" ", sorted(flat_, key=lambda x: x[1]))
    print((monotonic_ns() - t0)/1e9)