#!/usr/bin/env python

# ---------------------------
# CS 373 Project 3
# Anh-Khoi Dang - add562
# ---------------------------

# ----------------------------------------------------------
# Parsers for precomputed data
# These were ran once to generate precomputed files in extra/
# They will NOT be ran in normal execution
# See README.txt for usage
# ----------------------------------------------------------

from __future__ import with_statement
import sys, os, glob, re
from Netflix import netflix_parse_precomputed, netflix_decade_calc

def netflix_decade_avg (trainingSetDir):
    """
    Compute customer averages per decade that the movie was created.
    Print to standard out or redirect to file using "> extra/movieDecadeAvgRatings.in"
    trainingSetDir is the path to training_set/ from the command line
    """
    assert trainingSetDir
    movieIDYear = netflix_parse_precomputed('extra/movie_titles_no_nulls.txt', ',')
    
    # Build dict of dict of list {custID: {decade:[totalRating, numRatings]}}
    custIDDecade = {}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        #print file
        with open(file, 'r') as f_myfile:
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            for custIDRatingDateLine in lines[1:] :
                decadeDict = {'1890s':[0, 0],'1900s':[0, 0],'1910s':[0, 0],'1920s':[0, 0],'1930s':[0, 0],'1940s':[0, 0],'1950s':[0, 0],'1960s':[0, 0],'1970s':[0, 0],'1980s':[0, 0],'1990s':[0, 0],'2000s':[0, 0]}
                #get custID and actual rating
                custIDRatingDateList = custIDRatingDateLine.strip().split(',')
                custID = custIDRatingDateList[0]
                rating = float(custIDRatingDateList[1])
                assert 1.0 <= rating <= 5.0
                
                # Initialize dictionary 
                if not custID in custIDDecade:
                    custIDDecade[custID] = decadeDict
                else : # custID entry already exists, so add to that dict
                    decadeDict = custIDDecade[custID]
                
                #look up year
                year = movieIDYear[movieID]
                
                #determine the decade 
                decade = netflix_decade_calc(year)
                
                #add to that decade's [totalRating, numRatings]
                totalRatingNumRatingList = decadeDict[decade]
                totalRatingNumRatingList[0] += rating #totalRating
                totalRatingNumRatingList[1] += 1      #numRatings
                decadeDict[decade] = totalRatingNumRatingList
                custIDDecade[custID] = decadeDict
                
    # compute averages for each decade  
    for custID in custIDDecade :
        print custID + ":"
        decadeDict = custIDDecade[custID]
        for decade in decadeDict :
            totalRatingNumRatingList = decadeDict[decade]
            totalRating = totalRatingNumRatingList[0]
            if totalRating == 0 : #customer didn't rate any movies of that decade
                continue
            numRating = totalRatingNumRatingList[1]
            avgRating = totalRating / numRating
            print decade + "=" + str(avgRating)
    
def netflix_movie_avg (trainingSetDir):
    """
    Compute average rating for each movie
    Print to standard out or redirect to file using "> extra/movieIDAvgRatings.in"
    trainingSetDir is the path to training_set/ from the command line
    """
    assert trainingSetDir
    # Compute average ratings for each movie
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
            print movieID + "=" + str(average)
    
def netflix_cust_avg (trainingSetDir) :
    """
    Compute average rating for each customer
    Print to standard out or redirect to file using "> extra/custIDAvgRatings.in"
    trainingSetDir is the path to training_set/ from the command line
    """
    assert trainingSetDir
    # Compute customer averages using dictionary of list {custID: [totalRating, numRatings]}
    custIDTotalRatingDict = {}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        with open(file, 'r') as f_myfile:
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            for custIDRatingDateLine in lines[1:] :
                # To avoid memory overflow error, store and update total rating and number of ratings on the fly
                totalRatingNumRatingList = [0, 0]
                custIDRatingDateList = custIDRatingDateLine.strip().split(',')
                custID = custIDRatingDateList[0]
                rating = float(custIDRatingDateList[1])
                # key custID already exists, so add to that list
                if custID in custIDTotalRatingDict :
                    assert 1 <= int(custID) <= 2649429
                    assert 1.0 <= rating <= 5.0
                    totalRatingNumRatingList = custIDTotalRatingDict[custID]
                totalRatingNumRatingList[0] += rating #totalRating
                totalRatingNumRatingList[1] += 1      #numRatings
                custIDTotalRatingDict[custID] = totalRatingNumRatingList
                
    # compute averages for each customer
    for custID in custIDTotalRatingDict :
        totalRatingNumRatingList = custIDTotalRatingDict[custID]
        totalRating = totalRatingNumRatingList[0]
        numRating = totalRatingNumRatingList[1]
        avgRating = totalRating / numRating
        print custID + "=" + str(avgRating)