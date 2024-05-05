import warnings
import functools

def deprecated(func):
    '''
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    '''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        # turn off filter
        warnings.simplefilter('always', DeprecationWarning)

        warnings.warn("Call to DEPRECATED function {}.".format(func.__name__),\
                      category=DeprecationWarning,\
                      stacklevel=2)
        
        # reset filter
        warnings.simplefilter('default', DeprecationWarning)

        return func(*args, **kwargs)
    
    return new_func