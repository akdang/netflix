#!/usr/bin/env python

# ---------------------------
# CS 373 Project 3
# Anh-Khoi Dang - add562
# ---------------------------

# -------
# imports
# -------

import StringIO
import unittest

from Netflix import netflix_read, netflix_eval, netflix_solve
from RMSE import rmse

# -----------
# TestNetflix
# -----------

class TestNetflix (unittest.TestCase) :

    # -----
    # RMSE
    # -----

    def test_rmse (self) :
        v = rmse(['3', '3', '3'], ['3', '3', '3'])
        self.assert_(v == 0.0)

    def test_rmse2 (self) :
        v = rmse(['1', '1', '1', '1', '1'], ['5', '5', '5', '5', '5'])
        self.assert_(v == 4.0)
        
    def test_rmse3 (self) :
        v = rmse(['5', '3', '2', '4', '5'], ['2', '4', '3', '1', '2'])
        self.assert_(str(v) == '2.40831891576')
        
    def test_rmse4 (self) :
        v = rmse(['5', '3', '2', '4', '5', '1', '4', '1', '5', '1', '5', '1', '2', '4', '5', '1', '3', '4', '2', '4'], 
                 ['2', '1', '3', '1', '1', '2', '4', '3', '1', '2', '2', '3', '2', '1', '1', '3', '4', '1', '5', '3'])
        self.assert_(str(v) == '2.47991935353')

# ----
# main
# ----

print "TestNetflix.py"
unittest.main()
print "Done."
