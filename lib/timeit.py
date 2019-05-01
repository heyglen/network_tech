import time


def timeit(name=None):
    local_name = name
    def real_timeit(fn):
        
        name = local_name

        if name is None:
            name = fn.__name__

        def timed(*args, **kw):

            start = time.time()
            result = fn(*args, **kw)
            end = time.time()
            print('[timeit] {} took {}'.format(name, end - start))
            return result
        return timed
    return real_timeit