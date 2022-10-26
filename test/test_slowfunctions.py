#!/usr/bin/env python3
import unittest
from time import perf_counter as pc
from slowfunctions import slowfunction, slowfunctionsettings

class Testslowfunction(unittest.TestCase):
    def test_slowfunction(self):
        """ Test slowfunctions.slowfunction """
        # test time control
        sleeptime = 0.01
        loops = 10
        slowfunctionsettings['sleeptime'] = sleeptime
        tic = pc()
        for i in range(loops):
            slowfunction(1,2)
        toc = pc()
        self.assertTrue((toc-tic)<(1.1*loops*sleeptime))
        self.assertTrue((toc-tic)>(0.9*loops*sleeptime))
        
        # set time to fast
        slowfunctionsettings['sleeptime'] = 0

        # test argument flexibility
        argss = [(1,2),
                (1,2),
                (1,2),
                (3,4),
                (1,2)]

        for args in argss:
            # the first argument is a reconstruction of the logic inside the slowfunction function itself
            self.assertEqual(
                hash((tuple(args), tuple([]))),
                slowfunction(*args)
                )

        # test ability to pass keyword arguments and get consistent results
        hash1 = slowfunction(name="David", age=21)
        hash2 = slowfunction(age=21, name="David")
        self.assertEqual(hash1, hash2)
