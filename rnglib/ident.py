from numpy.linalg import norm
from rnglib.dlscore import array_scores

from rnglib.tools import progress


def distance(sequence_a, sequence_b, n):
    diff = array_scores(sequence_a, n) - array_scores(sequence_b, n)
    return norm(diff)


def compute_scores(sequences, max_n=4, c_sub=1, c_ins=1, c_del=1, c_trans=1, repeats=True):
    scores = []
    for s_a, s_b in progress(sequences):
        f_a = [array_scores(s_a, n, c_sub, c_ins, c_del, c_trans, repeats) for n in range(1, max_n + 1)]
        f_b = [array_scores(s_b, n, c_sub, c_ins, c_del, c_trans, repeats) for n in range(1, max_n + 1)]
        scores.append([f_a, f_b])
    return scores


def prepare(scores, feature_func=lambda a, b: [a, b]):
    def add_case(s_a, s_b, match):
        raw.append(feature_func(s_a, s_b))
        classes.append(match)

    raw, classes = [], []
    l = len(scores)
    for i, (s_a, s_b) in enumerate(scores):
        for j, (s_c, s_d) in enumerate(scores[:i + 1]):
            if i == j:
                add_case(s_a, s_b, 1)
            else:
                add_case(s_a, s_c, 0)
                add_case(s_a, s_d, 0)
                add_case(s_b, s_c, 0)
                add_case(s_b, s_d, 0)
    return raw, classes
