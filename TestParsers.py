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

from Netflix import netflix_parse_precomputed, netflix_decade_calc
from Parsers import netflix_decade_avg, netflix_movie_avg, netflix_cust_avg

# -----------
# TestNetflix
# -----------

class TestParsers (unittest.TestCase) :
    
    # --------
    # Parsers
    # --------

    def test_decade_avg(self):
        trainingSetDir = "test/1_movie_1_cust/"
        w = StringIO.StringIO()
        netflix_decade_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1:\n2000s=1.0\n')
        
    def test_decade_avg2(self):
        trainingSetDir = "test/5_movies_1_cust/"
        w = StringIO.StringIO()
        netflix_decade_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1:\n1990s=1.0\n2000s=1.0\n')
        
    def test_decade_avg3(self):
        trainingSetDir = "test/5_movies_5_cust/"
        w = StringIO.StringIO()
        netflix_decade_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '100:\n1990s=3.5\n2000s=2.66666666667\n200:\n1990s=3.5\n2000s=2.66666666667\n300:\n1990s=3.5\n2000s=2.66666666667\n400:\n1990s=3.5\n2000s=2.66666666667\n500:\n1990s=3.5\n2000s=2.66666666667\n')

    def test_movie_avg(self):
        trainingSetDir = "test/1_movie_1_cust/"
        w = StringIO.StringIO()
        netflix_movie_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1=1.0\n')
        
    def test_movie_avg2(self):
        trainingSetDir = "test/5_movies_1_cust/"
        w = StringIO.StringIO()
        netflix_movie_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1=1.0\n2=1.0\n3=1.0\n4=1.0\n5=1.0\n')
        
    def test_movie_avg3(self):
        trainingSetDir = "test/5_movies_5_cust/"
        w = StringIO.StringIO()
        netflix_movie_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1=1.0\n2=2.0\n3=3.0\n4=4.0\n5=5.0\n')
    
    def test_cust_avg(self):
        trainingSetDir = "test/1_movie_1_cust/"
        w = StringIO.StringIO()
        netflix_cust_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1=1.0\n')
        
    def test_cust_avg2(self):
        trainingSetDir = "test/5_movies_1_cust/"
        w = StringIO.StringIO()
        netflix_cust_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '1=1.0\n')
        
    def test_cust_avg3(self):
        trainingSetDir = "test/5_movies_5_cust/"
        w = StringIO.StringIO()
        netflix_cust_avg(trainingSetDir, w)
        self.assert_(w.getvalue() == '100=3.0\n200=3.0\n300=3.0\n400=3.0\n500=3.0\n')

# ----
# main
# ----

print "TestParsers.py"
unittest.main()
print "Done."
