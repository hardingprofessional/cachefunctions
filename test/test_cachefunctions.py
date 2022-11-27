#!/usr/bin/env python3
from cachefunctions import FunctionCache, cachefunction 
from os import unlink
from os.path import exists
import unittest
from time import perf_counter as pc

# set pickle location globally
fpath = "data/slowfunctioncache.pkl"

# define unittests
class TestCacheFunction(unittest.TestCase):
    
    def test_CacheFunction(self):
        """
        Test the CacheFunction class
        """

        # import slowfunctions and config
        from slowfunctions import slowfunction, slowfunctionsettings
        slowfunctionsettings['sleeptime'] = 0.25

        # if the file already exists, delete it
        if exists(fpath):
            unlink(fpath)

        # init the cache
        slowfunctioncache = FunctionCache(fpath)

        # this is how you decorate an imported function. Its weird.
        slowfunction = slowfunctioncache.decorator(slowfunction)

        # # this is provided for reference, how this would look normally
        # @slowfunctioncache.decorator
        # def myfunction(a, b):
        #     return a+b

        # basic arguments
        argss = [(1,2),
                (1,2),
                (1,2),
                (3,4),
                (1,2)]

        # 2 unique arguments should take no more than 0.5s+ds of run time
        tic = pc()
        for args in argss:
            slowfunction(*args)
        toc = pc()
        self.assertTrue((toc-tic)<0.6)
        
        # Test key word arguments
        lasthash = None
        for i in range(3):
            hashvalue = slowfunction(name="David")
            if lasthash is not None:
                self.assertTrue(lasthash==hashvalue)
            lasthash = hashvalue

        # save the cache and delete the object
        # to recreate nominal exit, we will delete the reference to slowfunction, 
        # then we will delete the slowfunctioncache object.
        # When the last reference to slowfunctioncache is gone, the slowfunctioncache.__del__()
        # method will call slowfunctioncache.save().
        del slowfunction
        del slowfunctioncache

        # delete the cache
        unlink(fpath)

    def test_reload(self):
        """
        Test case where function cache is reloaded.
        Simultaneously test case where functional form is used.
        """
        # import slowfunctions and config
        from slowfunctions import slowfunction, slowfunctionsettings
        slowfunctionsettings['sleeptime'] = 0.25

        # make a pickle file available with some cached data
        fc = FunctionCache(fpath)
        slowfunction = fc.decorator(slowfunction)
        slowfunction(1,2)
        del fc #deleting fc should trigger fc.save()
        del slowfunction

        # import slowfunctions and config
        from slowfunctions import slowfunction, slowfunctionsettings
        slowfunctionsettings['sleeptime'] = 0.25

        # decorate the slowfunction using functional syntax
        # I'd have liked to have had this:
        # @cachefunction(fpath)
        # def slowfunction(...): ...
        # but that doesn't work on imported functions
        slowfunction = cachefunction(fpath)(slowfunction)

        # run 10x with inputs (1,2)
        tic = pc()
        for i in range(10):
            slowfunction(1,2)
        toc = pc()
        self.assertTrue((toc-tic)<0.1)

        # if you don't delete references to slowfunctioncache, which are hidden inside the functioncache decorator, then another pickle will be generated when tests exit. To prevent this, trigger object deletion now.
        del slowfunction

        # clean up
        unlink(fpath)
