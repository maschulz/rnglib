import sys
import time


def sec_to_str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def progress(iterator, verbose=True, name=""):
    """
    progress bar wrapper for iterators

    used like this:
    >>> for i in progress(range(10)):
    >>>     sleep(1)
    >>>
    >>> [##################################################] 10/10 0:00:00

    :param iterator: iterator - needs to have len and next implemented
    :param verbose: bool - show progress bar?
    :param name: str - prefix the progress bar with a name / description
    :return: iterator
    """
    if not verbose:
        for item in iterator:
            yield item

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
