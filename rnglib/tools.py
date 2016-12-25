import sys
import time


def sec_to_str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def progress(iterator, name=""):
    length = len(iterator)
    size = 50
    timer = []

    def update(iteration):
        done = size * iteration // length

        timer.append(time.time())
        if len(timer) > 1:
            avg_time = mean(diff(timer))
            remaining_time = sec_to_str(avg_time * (length - iteration))
        else:
            remaining_time = "?:?:?"

        sys.stdout.write(
            "\r%s[%s%s] %i/%i %s" % (name, "#" * done, "." * (size - done), iteration, length, remaining_time))
        sys.stdout.flush()

    update(0)
    for i, item in enumerate(iterator):
        yield item
        update(i + 1)

    sys.stdout.write("\n")
    sys.stdout.flush()


from numpy import mean, diff, std, sqrt


def cohens_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx - 1) * std(x, ddof=1) ** 2 + (ny - 1) * std(y, ddof=1) ** 2) / dof)


def effect_size(classes, scores, ref_class=1):
    sa, di = [], []
    for i, j in zip(classes, scores):
        if i == ref_class:
            sa.append(j)
        else:
            di.append(j)
    return cohens_d(sa, di)
