# Introducting `cachefunctions`

This package is an alternative set of cachefunctions that include the ability to cache-to-disk.

If you want to cache a function and save the cache to disk, use this package.

If you want to cache a function but don't want to save the cache to disk, use `functools.cache` or `functools.lru_cache`.

# What is Caching?

Consider the following function:

``` python
from time import sleep
def myfunction(a, b):
    sleep(5)
    return a+b

# runtime takes 15 seconds
myfunction(1,2)
myfunction(2,3)
myfunction(1,2)
```

This function has the following properties:

1. It is deterministic, meaning given a specific set of inputs, the outputs will always be the same.
2. The function is slow.

We can add caching to this function by storing the return value in a dictionary and returning that value if the same inputs are provided in a subsequent call.:

``` python
from time import sleep
cache = dict()
def myfunction(a, b):
    try:
        return cache(a, b)
    except KeyError:
        sleep(5)
        return a+b

# runtime takes 10 seconds
myfunction(1,2)
myfunction(2,3)
myfunction(1,2) #pulled from cache
```

# Python's Standard Caches

Python ships with some caches in functools that you should use. These decorators can be easily applied to functions without re-writing their logic.

``` python
from functools import cache

@cache
def myfunction(a,b):
    return a+b
# runtime takes 10 seconds
myfunction(1,2)
myfunction(2,3)
myfunction(1,2) #pulled from cache
```

# Why use this package

Python's built in caches don't save to disk! You can speed up a single run of your script, but you cannot save that cache and use it to accelerate a subsequent run of the same script.

This package gives you the ability to create a cache file and save to it to disk, which may accelerate subsequent runs of your script.

``` python
from cachefunctions import cachefunction

@cachefunction("cachefile.pkl")
def myfunction(a,b):
    return a+b
# runtime takes 10 seconds on first run
# runtime takes 0 seconds on second run
myfunction(1,2) #loaded from cache on second run
myfunction(2,3) #loaded from cache on second run
myfunction(1,2) #loaded from cache on first run
```

This package also offers a class based API for creating and configuring function cache objects. 

``` python
from cachefunctions import CacheFunction

cf = CacheFunction("cachefile.pkl")
@cf.decorator
def myfunction(a,b):
    return a+b
# runtime takes 10 seconds on first run
# runtime takes 0 seconds on second run
myfunction(1,2)
myfunction(2,3)
myfunction(1,2)
```

# Use in rapid development

I do a lot of "data pipeline" type development, where the `__main__` block contains calls to functions that complete several steps. I use this toolkit to cache the results from steps I know are running correctly, so I can more quickly test parts I have just written.

``` python
from cachefunctions import cachefunction

@cachefunction("retrievemeasurements.pkl")
def retrievemeasurements()
    """ omitted for brevity """

@cachefunction("rangemeasurements2keplerianelements.pkl")
def rangemeasurements2keplerianelements()
    """ omitted for brevity """

def calculatenearestapproach()
    """ function actively being developed, so not cached """

if __name__ == "__main__":
    # retrievemeasurements runs instantly because the values were cached
    rangemeasurements = retrievemeasurements('a','b','c')
    # rangemeasurements2keplerianelements runs instantly because values were cached
    keplerianelements = rangemeasurements2keplerianelements(rangemeasurements)
    # This function runs slowly because I am developing it
    nearestapproach = calculatenearestapproach(keplerianelements, 'ISS')

    # I usually remove all caching decorators before delivering a product
```

# Requirements

This software is written in vanilla python, but the type hints require python 3.9+ to parse.

For a function to be cacheable by this package, it must meet the following properties:

1. The function must be deterministic (same inputs always yield same outputs)
2. Input arguments and keyword arguments must all be hashable
3. Input arguments and keyword arguments must all be serializable 
4. Return values must be serializable.

For a function to be a good candidate for use with this package:

1. The function must be called many times, with subsequent calls costing a significant amount of time.
2. The function must be called in subsequent runs of the python script. If (2) is not fulfilled, use functools.cache instead.

# Future

The following enhancements are possible, but I'll only implement them if needed.

cache file formats:

- [x] pickle
- [ ] sqlite
- [ ] json
- [ ] xml
- [ ] csv
- [ ] xlsx

cache properties

- [ ] maxentries
- [ ] maxbytes
- [ ] maxseconds

cache methods

- [ ] purgekey
- [ ] purgekeys (lambda)
- [ ] getkey
- [ ] getkeys (lambda)

I am *not* planning to store cached data in a memory object alternative to a dictionary.
This is a performance bottleneck, yes, but the alternative is to build something clever in C and code up a ctypes interface.
For this reason, functools will always provide better performance than cachefunctions.
