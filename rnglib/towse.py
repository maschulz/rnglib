import itertools
import math

combinations = itertools.product
D_SET = range(9)


def occurrence(z, m):
    """
    >>> occurrence([0,1,2,0,1,2,0],[0,1])
    [1, 4]
    """
    if type(m) == int: m = [m]
    if type(m) == tuple: m = list(m)
    r = []
    for i in range(len(m), len(z) + 1):
        if z[i - len(m):i] == m: r.append(i - 1)
    return r


def count(z, m):
    """
    >>> count([0,1,2,0,1,2,0],[0,1])
    2
    """
    return len(occurrence(z, m))


def mean(l):
    """
    >>> mean([0,1])
    0.5
    """
    return 1. * sum(l) / len(l)


def median(l):
    """
    >>> median([0,1,2])
    1
    """
    l.sort()
    return l[len(l) // 2]


def mode(l):
    """
    >>> mode([0,1,1,1,2])
    1
    """
    r = {}
    for i in l:
        if i in r:
            r[i] += 1
        else:
            r[i] = 1
    return max(r, key=lambda a: r.get(a))


def std(l):
    """
    >>> std([0,1,0,1])
    0.5
    """
    m = mean(l)
    return math.sqrt(sum([(i - m) ** 2 for i in l]) / len(l))


def redundancy(z, d=D_SET):
    """
    calculate redundancy of sequence z for set d
    *rgtcalc -> match*

    >>> redundancy([0,1],d=range(2))
    0.0
    >>> redundancy([0,0],d=range(2))
    1.0
    """
    a, n = len(d), len(z)
    h_max = math.log(a, 2)
    h = math.log(n, 2)
    for i in d:
        if count(z, i) is not 0:
            h -= (count(z, i) * math.log(count(z, i), 2)) / n
    return 1 - h / h_max


# todo:fix coupon score!!!
def coupon(z, d=D_SET):
    """
    calculate coupon score of sequence z
    *rgtcalc -> rgtcalc wrong!? const lag -2*

    >>> coupon([1,2,3,4,5,6,7,8,0])
    (9.0, 0.0)
    """

    def fin(t):
        for i in d:
            if not i in t: return False
        return True

    res = []
    for i in range(len(z)):
        tmp = []
        for j in range(len(z) - i):
            tmp.append(z[i + j])
            if fin(tmp):
                res.append(j + 1)
                break
    if not res: return {'mean': len(z) + 1, 'std': len(z) + 1}
    # print res
    return {'mean': mean(res), 'std': std(res)}


def repetition_gap(z, d=D_SET):
    """
    calculate coupon score of sequence z
    *rgtcalc -> match*

    >>> repetition_gap([1,2,3,4,3,2,1])
    (4.0, 4, 2, 1.6329931618554521)
    """
    r = []
    for i in d:
        t = occurrence(z, i)
        for k in range(1, len(t)):
            r.append(t[k] - t[k - 1])
    return {'mean': mean(r), 'median': median(r), 'mode': mode(r), 'std': std(r)}


def rng(z, d=D_SET):
    """
    log base?
    formula errata?
    *rgtcalc -> match*
    >>> rng([0,1,2,3,4,1,1,1])
    0.33333333333333337
    """
    r = dict([(i, count(z, i)) for i in combinations(d, repeat=1)])
    r.update(dict([(i, count(z, i)) for i in combinations(d, repeat=2)]))
    s = [0., 0.]
    for i in d:
        for j in d:
            if not r[(i, j)]: continue
            s[0] += r[(i, j)] * math.log(r[(i, j)])
            s[1] += r[(i, j)] * math.log(r[(i,)])
    return s[0] / s[1]


def rng2(z, d=D_SET):
    """
    log base?
    formula errata?
    *rgtcalc -> match*
    >>> rng2([1,2,1,2,1,2,3,4,5])
    0.42061983571430489
    """

    def gap_count(z, m):
        r = 0
        for i in range(len(z) - 2):
            if (z[i], z[i + 2]) == m: r += 1
        return r

    r = dict([(i, count(z, i)) for i in combinations(d, repeat=1)])
    r.update(dict([(i, gap_count(z, i)) for i in combinations(d, repeat=2)]))
    s = [0., 0.]
    for i in d:
        for j in d:
            if not r[(i, j)]: continue
            s[0] += r[(i, j)] * math.log(r[(i, j)])
            s[1] += r[(i, j)] * math.log(r[(i,)])
    return s[0] / s[1]


def adjacent(z, d=D_SET):
    """
    *rgtcalc -> match*
    >>> adjacent([1,2,1,2,1,2,3,4,5])
    (0.75, 0.25, 1.0)
    """
    up, down = 0., 0.
    for i in range(len(z) - 1):
        if z[i] + 1 == z[i + 1]: up += 1
        if z[i] - 1 == z[i + 1]: down += 1
    r = up / (len(z) - 1), down / (len(z) - 1)
    return {'asc': r[0], 'desc': r[1], 'comb': sum(r)}


# FIXME
def tpi(z, d=D_SET):
    """
    *rgtcalc -> match*
    >>> tpi([1,2,3,2,1])
    1.5
    """
    t = 0.
    length = len(z)
    z = [z[i - 1] - z[i] for i in range(1, len(z))]
    # z = filter(lambda x: x, z) # ???
    for i in range(1, len(z)):
        if z[i - 1] < 0 < z[i]: t += 1
        if z[i - 1] > 0 > z[i]: t += 1
    t_e = 2. / 3. * (length - 2)
    return t / t_e


def runs(z, func, d=D_SET):
    """
    >>> runs([1,2,3,4,5,6,7,1,2,3,4], lambda x: x<0)
    [6, 3]
    """
    r = []
    i = 0
    while i < len(z):
        j = 1
        while i + j < len(z) and func(z[i + j - 1] - z[i + j]):
            j += 1
        if j > 1:
            r.append(j - 1)
            i = i + j
        else:
            i += 1
    return r


def runups(z, d=D_SET):
    r = runs(z, lambda x: x < 0, d=D_SET)
    return {'mean': mean(r), 'std': std(r)}


def rundowns(z, d=D_SET):
    r = runs(z, lambda x: x > 0, d=D_SET)
    return {'mean': mean(r), 'std': std(r)}


def cs1(z, d=D_SET):
    """
    summe!!
    """
    r = runs(z, lambda x: x == -1, d=D_SET)
    r = map(lambda x: x ** 2, r)
    return {'mean': mean(r), 'std': std(r), 'sum': sum(r)}


# return sum(r)

def cs2(z, d=D_SET):
    r = runs(z, lambda x: x == -2, d=D_SET)
    r = map(lambda x: x ** 2, r)
    # return {'mean': mean(r), 'std': std(r), 'sum': sum(r)}
    return sum(r)


def phi(z, n, d=D_SET):
    """
    *rgtcalc -> hmm... who is wrong here? description is *!#!$ bad; solution: see comment*
    >>> phi([1,2,3,4,3,2,1,2,3,4], 5)
    0.10710323391385287
    """
    r_s, r_d = [0., 0.], [0., 0.]
    t_o, t_e = 0., 0.
    z_raw = z[:]
    for w in d:
        z = map(lambda x: int(x == w), z_raw)
        for i in combinations([0, 1], repeat=n):
            t_e = 1. * (count(z, i[1:]) * count(z, i[:-1]))
            if not t_e: continue
            if n == 2:
                t_e /= len(z)
            else:
                t_e /= count(z, i[1:-1])

            t_o = count(z, i)

            if i[0] == i[-1]:
                r_s[0] += t_o
                r_s[1] += t_e
            else:
                r_d[0] += t_o
                r_d[1] += t_e
                # print w, i, t_o, t_e
                # print r_s, r_d
    chi = (r_s[0] - r_s[1]) ** 2 / r_s[1] + (r_d[0] - r_d[1]) ** 2 / r_d[1]
    # return math.sqrt(chi/(len(z)*2*len(d))) this is what towse did. i have no idea why.
    return math.sqrt(chi / (len(z) * len(d)))
