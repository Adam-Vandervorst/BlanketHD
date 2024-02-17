from bhv.native import NativePackedBHV as BHV, DIMENSION


def outside(self, vs: 'list[Self]', d: int) -> list[int]:
    return list(filter(lambda i: BHV.hamming(self, vs[i]) > d, range(len(vs))))


def outside_std(self, vs: 'list[Self]', d: float, relative: bool = False) -> list[int]:
    return outside(self, vs, int(DIMENSION * (self.std_to_frac(d + self.EXPECTED_RAND_APART * relative))))


class ATree:
    def __init__(self, parents):
        self.parents: list[int] = parents

    def size(self):
        return len(self.parents)

    def parent(self, i):
        return self.parents[i]

    def children(self, i):
        return [j for j, p in enumerate(self.parents) if p == i]

    def path(self, i):
        p = [i]
        while True:
            a = self.parents[p[-1]]
            if a == p[-1]:
                return p
            p.append(a)

    def leaves(self):
        ps = set(self.parents)
        return [i for i in range(len(self.parents)) if i not in ps]

    def lower(self, i):
        return [j for j in range(len(self.parents)) if i in self.path(j)]


class HDCTree:
    def __init__(self, values, parents):
        self.values = values
        self.v = BHV.majority(values)
        self.d = BHV.majority([values[k] ^ values[p].permute(1) for k, (v, p) in enumerate(zip(values, parents))])

    def parent(self, i):
        return (self.values[i] ^ self.d).permute(-1).closest(self.values)

    def children(self, i):
        return (self.values[i].permute(1) ^ self.d).within_std(self.values, -4., relative=True)

    def path(self, i):
        pv = [self.values[i]]
        for i in range(3):
            av = (pv[-1] ^ self.d).permute(-1)
            pv.append(av)
        print(len(pv))
        return pv[3].within_std(self.values, -3, relative=True)

    def leaves(self):
        return outside_std((self.d ^ self.v).permute(-1), self.values, -3, relative=True)

    def lower(self, i):
        return ((self.values[i].permute(1) ^ self.d).permute(1) ^ self.d).within_std(self.values, -4., relative=True)


if __name__ == '__main__':
    x = ATree([0, 0, 1, 1, 0, 4, 5, 5, 5])

    assert x.parent(5) == 4
    assert x.children(5) == [6, 7, 8]
    assert x.path(6) == [6, 5, 4, 0]
    assert x.leaves() == [2, 3, 6, 7, 8]
    assert x.lower(1) == [1, 2, 3]

    x_ = HDCTree(BHV.nrand(9), x.parents)

    assert x_.parent(5) == 4
    assert x_.children(5) == [6, 7, 8]
    # print(x_.path(6))
    assert x_.leaves() == [2, 3, 6, 7, 8]
    print(x_.lower(1))
    print(x_.lower(4))


