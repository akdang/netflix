#!/usr/bin/env python

# ---------------------------
# CS 373 Project 3
# Anh-Khoi Dang - add562
# ---------------------------

# -------
# imports
# -------

import sys, time

from Netflix import netflix_read, netflix_eval, netflix_solve


# ----
# main
# ----
#s = time.clock()

if len(sys.argv) != 4 : 
    exit("Usage: python RunNetflix.py <movie titles file> <training set directory> <probe file>")
else :
    movieTitlesFile = sys.argv[1]
    trainingSetDir = sys.argv[2]
    probeFile = sys.argv[3]
    
netflix_solve(sys.stdout, trainingSetDir, probeFile)

#e = time.clock()
#print (e - s), "seconds"