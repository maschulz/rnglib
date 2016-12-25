from numpy import mean, std
from rnglib.dlscore import array_scores

from rnglib.tools import progress


def compute_scores(sequences, max_n=4, c_sub=1, c_ins=1, c_del=1, c_trans=1, repeats=True, scale=True):
    """
    compute score matrix for list of sequence pairs

    :param sequences: [[s0_0, s0_1],[s1_0,s1_1],...] - list of sequence pairs, one pair per subject
    :param max_n: int - calculate scores for patterns up to length max_n
    :param repeats: bool - allow patterns containing repeats?
    :return: scores(float) in list[subjects][sequence_index][pattern_length-1][pattern_index]
    """
    scores = []
    for s_a, s_b in progress(sequences):
        f_a = [array_scores(s_a, n, c_sub, c_ins, c_del, c_trans, repeats) for n in range(1, max_n + 1)]
        f_b = [array_scores(s_b, n, c_sub, c_ins, c_del, c_trans, repeats) for n in range(1, max_n + 1)]
        scores.append([f_a, f_b])

    if scale:
        print('scaling: ', end='')
        for n in range(max_n):
            all_scores = [i[n] for i, j in scores] + [j[n] for i, j in scores]
            mu = mean(all_scores, 0)
            sd = std(all_scores, 0)
            for i, j in scores:
                for k in [i, j]:
                    k[n] -= mu
                    k[n] /= sd
            print('%i. ' % n, end='')
        print()
    return scores


def prepare(scores, feature_func=lambda a, b: [a, b]):
    """
    prepare scores for classification

    create cartesian product of sequences with class labels (1 - same subject, 0 - different subjects)
    process each pair via feature_func(s_a[pattern_length-1][pattern_index], s_b[pattern_length-1][pattern_index])
    e.g. lambda a, b: norm(a[2]-b[2]) returns length-3 score-distance as sole feature
    lambda a, b: a[2]-b[2] returns length-3 score-array features

    :param scores: score matrix - from compute_scores()
    :param feature_func: function(score_array, score_array)
    :return: list of features, list of classes
    """

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