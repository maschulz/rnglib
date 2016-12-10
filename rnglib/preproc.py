import random


def chunks(l, n, off=0):
    assert off < n
    assert n > 0
    t = [l[:off]] + [l[i + off:i + n + off] for i in range(0, len(l) - off, n)]
    return [i for i in t if len(i)]


def chunk_shuffle(z, n):
    c = chunks(z, n, random.randint(0, n - 1))
    random.shuffle(c)
    r = []
    for i in c: r.extend(i)
    return r
