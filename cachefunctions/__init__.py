"""
This module contains the cachefunction() decorator and the CacheFunction() decorator class. The purpose of these cache objects is to support generic function caching with a save-to-disk feature.
"""

import pickle as pkl
from pathlib import Path
import atexit
from functools import wraps
from typing import Callable, Any, Union

# globals
# type hints
TypeGenericFunction = Callable[Any,Any]
TypeStrPath = Union[str,Path]

# functions
def dict2tuple(di:dict) -> tuple :
    """ 
    Converts a dictionary into a tuple of 2-element tuples, where each pair of elements is (key,value) and each of the 2-element tuples is sorted().
    This is mainly done to make a dictionary hashable, but that only works if all keys and values are hashable and sortable.

    :param di: the dictionary to convert from {k1:v1,k2:v2} to [(k1, v1), (k2,v2)]
    :return: a tuple of the form ((k1, v1), (k2,v2))
    """
    return tuple([(key, value) for key,value in sorted(di.items(), key=lambda x: x[0])])

def cachefunction(fname:TypeStrPath) -> TypeGenericFunction:
    """
    Simple decorator.
    Rather than making the user manage a FunctionCache object, this simple decorator allows you to just specify a file name and go. It uses the FunctionCache object under-the-hood, and those features are not accessible through this decorator function. For access to the full feature set, use the class based decorator pattern.

    :param fun: function to decorate
    :param fname: file to store cache in at runtime exit
    :return: The same function, but with caching enabled
    """
    def wrap(fun:TypeGenericFunction) -> TypeGenericFunction:
        # init function class object
        fc = FunctionCache(fname)
        # return decorated function
        return fc.decorator(fun)
    return wrap

# classes
class FunctionCache:
    """
    Provides a decorator for your cacheable function.
    A function is cacheable if:
    1. The inputs are hashable
    2. The function always returns the same output given the same inputs.
    A function is a good candidate for caching if:
    1. It takes a long time per call
    2. It is called frequently

    If you do not want to cache the function responses to disk, then use the standard python functools.cache() or functools.lru_cache. 

    If you want to maintain a cache after the program terminates, for use on the next run, then use this class.

    To use this class, do the following:

    # init a global FunctionCache object for each cached function
    myfunccache = FunctionCache('myfunccache.pkl')

    # decorate your function with the function decorator
    @myfunccache.decorator
    def myfunc():
        ....

    # to decorate an imported function
    from slowfunction import slowfunction
    slowfunction = myfunccache.decorator(slowfunction)
    """
    # prevent the `open` builtin from being garbage collected before this class
    open = open

    def __init__(self, fpath:TypeStrPath):
        """
        Initialize a FunctionCache object.

        :param fpath: A Path or pathlike string to a cache object pickle
        """
        self.fpath = Path(fpath)
        # handle the file access
        self._setupfile()

        # various settings
        self.savebeforedelete=True

    def _setupfile(self) -> None:
        """
        Verifies that self.fpath is valid. 
        If self.fpath does not exist, a new cache is created that will be saved to that location.
        If self.fpath does exist and is a file, it will be treated as a cache and loaded.
        If self.fpath does exist and is not a file, an error will be thrown.
        """
        # if fname exists:
        if self.fpath.exists():
            # if fname is a file:
            if self.fpath.is_file():
                # load the file to self._cache
                with open(self.fpath, 'rb') as f:
                    self._cache = pkl.load(f)
            # if fname is not a file, throw an error
            else:
                raise Exception(f"{self.fpath} exists and is not a file")
        # if fname does not exist, start a new cache dictionary
        else:
            self._cache = dict()

    def _makekey(self, *args:Any, **kwargs:Any) -> tuple:
        """
        makes a valid key from a functions arguments, assuming all arguments are hashable.
        :param *args: a tuple of arguments
        :param **kwargs: a dictionary of keywords
        :return: given (a1, a2, k1=v1, k2=v2), returns ((a1, a2), ((k1,v1),(k2,v2)))
        """
        return (args, dict2tuple(kwargs))

    def decorator(self, fun:TypeGenericFunction) -> TypeGenericFunction:
        """
        The decorator method is used as a decorator.
        
        ``` python
        # common pattern
        @fc.decorator
        def myfunction():
            ...
        ```

        ``` python
        # alternative pattern
        myfunction = fc.decorator(myfunction)
        ```

        :param fun: The function you intend to decorate
        """
        @wraps(fun) #used to preserve wrapped function properties like __doc__
        def inner_function(*args, **kwargs):

            # convert args and kwargs into a cacheable argument
            cachekey = self._makekey(*args, **kwargs)
            
            # attempt to retrieve the cached result
            try:
                return self._cache[cachekey]
            
            # if the inputs aren't cached, run the function and cache the result
            except KeyError:
                result = fun(*args, **kwargs)
                self._cache[cachekey] = result
                return result

            # Usually hit this if an argument is an uncacheable type
            except TypeError:
                print("handle uncacheable keys smarter")
                breakpoint()
            
        return inner_function
    
    def save(self) -> None:
        """ saves the cache to self.fpath """
        with self.open(self.fpath, 'wb') as f:
            pkl.dump(self._cache, f)

    def __del__(self) -> None:
        """ calls self.save() before deleting class object """
        if self.savebeforedelete:
            self.save()


