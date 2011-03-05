#!/usr/bin/env python

# -------
# RMSE.py
# -------

def rmse (a, p) :
    rating_dict = {'1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5}
    assert type(a) == list
    assert type(p) == list
    assert len(a) == len(p)
    i = 0
    s = len(a)
    w = 0
    while i != s :
        v = rating_dict[a[i]] - float(p[i])
        w += (v ** 2)
        i += 1
    assert type(w) is float
    assert 0 <= w <= (16 * s)
    m = (w / s)
    assert type(m) is float
    assert 0 <= m <= 16
    r = (m ** .5)
    assert type(r) is float
    assert 0 <= r <= 4
    return r
    
def square_of_difference(x, y) :
  rating_dict = {'1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5}
  actual = rating_dict[x]
  assert type(actual) is int
  pred = float(y)
  sd = (actual - pred) ** 2
  assert type(sd) is float
  return sd
  
def mean(a) :
  assert type(a) is list
  m = sum(a) / len(a)
  assert 0 <= m <= 16
  return m
    
def rmse2(a,p) :
  assert type(a) is list
  assert type(p) is list
  assert len(a) == len(p) 
  r = mean(map(square_of_difference, a, p)) ** .5
  assert 0 <= r <= 4
  return r
