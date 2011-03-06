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

from Netflix import netflix_read, netflix_eval, netflix_solve, netflix_decade_calc, netflix_actual_ratings, netflix_parse_train, netflix_parse_precomputed
from RMSE import rmse, mean, square_of_difference

# -----------
# TestNetflix
# -----------

class TestNetflix (unittest.TestCase) :
    
    # --------
    # Helpers
    # --------
    def test_parse_train(self):
        trainingSetDir = 'test/1_movie_1_cust'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'1': '1'}})
    
    def test_parse_train2(self):
        trainingSetDir = 'test/5_movies_5_cust/'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'300': '1', '200': '1', '100': '1', '500': '1', '400': '1'}, '3':{'300': '3', '200': '3', '100': '3', '500': '3', '400': '3'}, '2': {'300': '2', '200': '2', '100': '2', '500': '2', '400': '2'}, '5': {'300': '5', '200': '5', '100': '5', '500': '5', '400': '5'}, '4': {'300': '4', '200': '4', '100': '4', '500': '4', '400': '4'}})
    
    def test_parse_train3(self):
        trainingSetDir = 'test/5_movies_1_cust/'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'1': '1'}, '3': {'1': '1'}, '2': {'1': '1'}, '5': {'1': '1'}, '4': {'1': '1'}})
    
    def test_actual_ratings(self):
        probeFile = 'test/1_movie_1_cust/probe.txt'
        trainingSetDir = 'test/1_movie_1_cust'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'1': '1'}})
        
        actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
        self.assert_(actualRatings == ['1'])
        
    def test_actual_ratings2(self):
        probeFile = 'test/5_movies_5_cust/probe.txt'
        trainingSetDir = 'test/5_movies_5_cust/'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'300': '1', '200': '1', '100': '1', '500': '1', '400': '1'}, '3':{'300': '3', '200': '3', '100': '3', '500': '3', '400': '3'}, '2': {'300': '2', '200': '2', '100': '2', '500': '2', '400': '2'}, '5': {'300': '5', '200': '5', '100': '5', '500': '5', '400': '5'}, '4': {'300': '4', '200': '4', '100': '4', '500': '4', '400': '4'}})
        
        actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
        self.assert_(actualRatings == ['1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '3', '3', '3', '3', '3', '4', '4', '4', '4', '4', '5', '5', '5', '5', '5'])
        
    def test_actual_ratings3(self):
        probeFile = 'test/5_movies_1_cust/probe.txt'
        trainingSetDir = 'test/5_movies_1_cust/'
        movieIDDict = netflix_parse_train(trainingSetDir)
        self.assert_(movieIDDict == {'1': {'1': '1'}, '3': {'1': '1'}, '2': {'1': '1'}, '5': {'1': '1'}, '4': {'1': '1'}})

        actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
        self.assert_(actualRatings == ['1', '1', '1', '1', '1'])
        
    def test_decade(self):
        year = '1890'
        self.assert_(netflix_decade_calc(year) == '1890s')
    
    def test_decade2(self):
        year = '2005'
        self.assert_(netflix_decade_calc(year) == '2000s')
    
    def test_decade3(self):
        year = '1989'
        self.assert_(netflix_decade_calc(year) == '1980s')
    
    # -----
    # RMSE
    # -----
    def test_mean(self):
        a = [2]
        self.assert_(mean(a) == 2)

    def test_mean2(self):
        a = [1, 2, 3]
        self.assert_(mean(a) == 2)
    
    def test_mean3(self):
        a = [1.2, 3.2, 4.4, 1.5, 2.8, 1.1, 2.1, 4.3, 4.8, 2.2, 3.2]
        self.assert_(round(mean(a),1) == 2.8)
    
    def test_sd(self):
        x = '1'
        y = '1.0'
        self.assert_(square_of_difference(x, y) == 0.0)
    
    def test_sd2(self):
        x = '3'
        y = '1.5'
        self.assert_(square_of_difference(x, y) == 2.25)
    
    def test_sd3(self):
        x = '5'
        y = '1.0'
        self.assert_(square_of_difference(x, y) == 16.0)

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
