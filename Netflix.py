#!/usr/bin/env python

# ---------------------------
# CS 373 Project 3
# Anh-Khoi Dang - add562
#
# ---------------------------

# -------
# imports
# -------

from __future__ import with_statement
import sys, os, glob


# ------------
# netflix_read
# ------------

def netflix_read (r, trainingSetDir) :
    """
    reads the input and parses it into preference dictionaries
    r is a reader
    numCouples is the number of couples
    isWomen indicates if we're iterating over women input
    return a list of [dict (person, array of preferences) pairs, and dict women ranks]
    """
    
    #netflix_train(trainingSetDir)
    
    # Create dictionary of (movie ID, average rating) from precomputed file
    movieIDAvgRating = {}
    with open('extra/movieIDAvgRatings.in', 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines :
            movieIDAvgRatingsList = line.strip().split('=')
            movieID = movieIDAvgRatingsList[0]
            average = movieIDAvgRatingsList[1]
            movieIDAvgRating[movieID] = average
    
    #print len(movieIDAvgRating)
    assert movieIDAvgRating
    return movieIDAvgRating

def netflix_train (trainingSetDir):
    # Compute average ratings for each movie
    movieIDAvgRating = {}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        average = 0.0
        totalStars = 0.0
        with open(file, 'r') as f_myfile:
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            numRatings = len(lines) - 1
            for custIDRatingDateLine in lines[1:] :
                custIDRatingDateList = custIDRatingDateLine.strip().split(',')
                totalStars += float(custIDRatingDateList[1])
            average = totalStars / numRatings
            assert 1.0 <= average <= 5.0
            assert 1 <= int(movieID) <= 17770
            movieIDAvgRating[movieID] = average
            print movieID + "=" + str(average)

# ------------
# netflix_eval
# ------------

def netflix_eval (w, movieIDAvgRating, probeFile) :
    """
    Attempts to match the men with the women such that if a man m
    prefers some woman w more than his wife, then w likes her 
    fiance more than m
    womenPrefs is a dictionary of (women, array of preferences) pairs
    menPrefs is a dictionary of (men, array of preferences) pairs
    return the engaged (men, women) pairs
    """
    import re
    # Iterate through probe file and make predictions
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        movieID = ""
        for line in lines :
            # Look for movieID
            if re.search(':$', line) :
                movieID = line.strip(':\r\n')
                print movieID
            else :
                assert movieID
                #custID
                #custID = line.strip()
                pred = movieIDAvgRating[movieID]
                print pred
                
# -------------
# netflix_print
# -------------

def netflix_print (w, movieID, isMovieID = False, pred = 0.0) :
    """
    prints the key-value pairs of engaged men to women
    w is a writer
    engagedMen is the dictionary of engaged (men, women)
    """
    if isMovieID :
        w.write(movieID + ":\n")
    else :
        w.write(str(pred) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    if len(sys.argv) != 4 : 
        exit("Usage: python RunNetflix.py <movie titles file> <training set directory> <probe file>")
    else :
        movieTitlesFile = sys.argv[1]
        trainingSetDir = sys.argv[2]
        probeFile = sys.argv[3]
    
    movieIDAvgRating = {}
    movieIDAvgRating = netflix_read(r, trainingSetDir)
    netflix_eval(w, movieIDAvgRating, probeFile)

    
        






