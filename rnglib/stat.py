from numpy import mean, std, sqrt, asarray, arange, tri

from rnglib.tools import progress


def cohens_d(x, y):
    """
    return cohens d

    :param x: list[float]
    :param y: list[float]
    :return: float
    """
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx - 1) * std(x, ddof=1) ** 2 + (ny - 1) * std(y, ddof=1) ** 2) / dof)


def effect_size(classes, scores, ref_class=1):
    """
    one-verus-rest effect size (cohens d)

    :param classes: int/str - list of class labels
    :param scores: float - list of samples
    :param ref_class: int/str - class to test
    :return: float - cohens d
    """
    sa, di = [], []
    for i, j in zip(classes, scores):
        if i == ref_class:
            sa.append(j)
        else:
            di.append(j)
    return cohens_d(sa, di)


def jackknife(data, func, verbose=False):
    """
    perform jackknife estimation of function on data set

    :param data: list of samples
    :param func: function that operates on list of samples and returns one or more values
    :param verbose: show progress bar
    :return: returns estimation and standard error
    """
    data = asarray(data)
    N = len(data)
    r = []
    idx = arange(1, N) - tri(N, N - 1, -1).astype('int')
    for i in progress(idx, verbose):
        r.append(func(data[i]))
    mu = mean(r, 0)
    se = sqrt((N - 1) / N * sum((asarray(r) - mu) ** 2, 0))
    return mu, se
