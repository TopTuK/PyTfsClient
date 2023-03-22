def batch(iterable, n=1):
    """
    "batch" function that would take as input an iterable and return an iterable of iterables
    https://stackoverflow.com/a/8290508/6753144
    """
    len_ = len(iterable)
    for ndx in range(0, len_, n):
        yield iterable[ndx:min(ndx + n, len_)]