#!/usr/bin/env python3
"""
I discovered several bugs related to python teardowns.
This test script is only valid if called directly with `python testteardowns.py`.
I include it in the unit test system because I'd like to work around this limitation in the future.
"""

from cachefunctions import cachefunction 
from os import unlink
from os.path import exists

# set pickle location globally
fpath = "data/teardown.pkl"

if __name__ == "__main__":
    # start without a pickle file
    if exists(fpath):
        unlink(fpath)
    # create a function to cache
    @cachefunction(fpath)
    def add2(a,b):
        return a+b
    # run the test case
    add2(1,2)
    add2(1,2)
    # DO NOT CLEAN UP, this would prevent the race condition I am trying to test
    # unlink(fpath)
    # program exit
    print("program execution complete")
