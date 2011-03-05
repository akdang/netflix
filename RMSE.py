#!/usr/bin/env python

# -------
# RMSE.py
# -------

def square_of_difference(x, y) :
    """
    Creates a list of actual ratings based on probe.txt for RMSE calculations
    probeFile is the path to probe.txt from the command line
    movieIDDict is a dictionary of dictionaries {movieID:{custID:rating}}
    return a list of actual ratings
    """
    rating_dict = {'1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5}
    actual = rating_dict[x]
    pred = float(y)
    sd = (actual - pred) ** 2
    assert type(sd) is float
    return sd
  
def mean(a) :
    assert type(a) is list
    m = sum(a) / len(a)
    assert 0 <= m <= 16
    return m
    
def rmse(a,p) :
    assert type(a) is list
    assert type(p) is list
    assert len(a) == len(p) 
    r = mean(map(square_of_difference, a, p)) ** .5
    assert 0 <= r <= 4
    return r
