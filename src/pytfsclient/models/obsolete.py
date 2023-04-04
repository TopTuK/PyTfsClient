import warnings
import functools

def obsolete(func):
    '''
    This is a decorator which can be used to mark functions
    as obsolete. It will result in a warning being emitted
    when the function is used.
    '''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        # turn off filter
        warnings.simplefilter('always', FutureWarning)

        warnings.warn("Call to OBSOLETE function {}.".format(func.__name__),\
                      category=FutureWarning,\
                      stacklevel=2)
        
        # reset filter
        warnings.simplefilter('default', FutureWarning)

        return func(*args, **kwargs)
    
    return new_func