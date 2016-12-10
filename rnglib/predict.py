import numpy as np
import scipy

from rnglib.dlscore import score as default_score

ai = lambda l: np.array(l, dtype='i')


class model(object):
    def __init__(self, base, n, d=range(9), score_func=default_score):
        self.base = ai(base)
        self.n = n
        self._cache = {}
        self._d = d
        self._score_func = score_func

    def get_score(self, pattern):
        pattern = tuple(pattern)
        if not pattern in self._cache:
            score = self._score_func(ai(pattern), self.base)
            self._cache[pattern] = score
        return self._cache[pattern]

    def scores(self, pattern):
        d = {}
        for i in self._d:
            d[i] = self.get_score(pattern + [i])
        return sorted(d, key=d.get, reverse=True)

    def predict(self, target):
        res = []
        for i in range(self.n, len(target)):
            pattern = target[i - self.n:i]
            next = target[i]
            pdf = self.scores(pattern)
            index = pdf.index(next)
            res.append(index)
        return res

    def stat(self, target):
        r = self.predict(target)
        return scipy.mean(r), r.count(0) / len(r)
