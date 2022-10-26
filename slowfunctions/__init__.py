#!/usr/bin/env python3
"""
This module contains a slow function for use with cache testing
"""

from time import sleep

slowfunctionsettings = { 
    "sleeptime":1,
    "verbose":False}

def slowfunction(*args, **kwargs):
    """slow function behavior is controlled through module level dictionary slowfunction.slowfunctionsettings"""
    argtuple = ( \
        tuple(args), \
        tuple([(key,value) for key,value \
            in sorted(kwargs.items(), key=lambda x : x[0])])
        )
    hashvalue = hash(argtuple)

    if slowfunctionsettings['verbose']:
        print(f"slowfunction args:{argtuple}, sleep for {slowfunctionsettings['sleeptime']}")
    sleep(slowfunctionsettings["sleeptime"])
    return hashvalue

if __name__ == "__main__":
    slowfunctionsettings['verbose'] = True
    slowfunction(1,2,3,cat="tabby",frog="prince")
