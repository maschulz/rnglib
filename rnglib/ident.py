from numpy.linalg import norm
from rnglib.dlscore import array_scores

from rnglib.tools import progress


def distance(sequence_a, sequence_b, n):
    diff = array_scores(sequence_a, n) - array_scores(sequence_b, n)
    return norm(diff)


def prepare(sequences):
    raw, classes = [], []
    l = len(sequences)
    for i, (s_a, s_b) in enumerate(sequences):
        for j, (s_c, s_d) in enumerate(sequences[:i + 1]):
            if i == j:
                raw.append([s_a, s_b])
                classes.append(1)
            else:
                raw.append([s_a, s_c])
                classes.append(0)
                raw.append([s_a, s_d])
                classes.append(0)
                raw.append([s_b, s_c])
                classes.append(0)
                raw.append([s_b, s_d])
                classes.append(0)
    return raw, classes


def compute(raw, diff_func):
    distances = []
    for s_a, s_b in progress(raw):
        distances.append(diff_func(s_a, s_b))
    return distances
