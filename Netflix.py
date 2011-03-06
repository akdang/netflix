#!/usr/bin/env python

# ---------------------------
# CS 373 Project 3
# Anh-Khoi Dang - add562
# ---------------------------

# -------
# imports
# -------

from __future__ import with_statement
from RMSE import rmse
import sys, os, glob, re


# ------------
# netflix_read
# ------------

def netflix_read (probeFile, trainingSetDir) :
    """
    Creates dictionaries from precomputed cache files
    Also parses training set and probe files to build actual ratings list
    probeFile is the path to probe.txt from the command line
    trainingSetDir is the path to the training_set directory from the command line
    return a list containing the average ratings based on movies and customers and the actual ratings
    """
    
    # Create dictionary of (movie ID, year) from input file
    movieIDYear = {}
    netflix_parse_precomputed(movieIDYear, 'extra/movie_titles_no_nulls.txt', ',')
    netflix_decade_avg(movieIDYear, trainingSetDir)
    
    # Create dictionary of (movie ID, average rating) from precomputed file
    movieIDAvgRating = {}
    netflix_parse_precomputed(movieIDAvgRating, 'extra/movieIDAvgRatings.in')
    
    # Create dictionary of (cust ID, average rating) from precomputed file
    custIDAvgRating = {}
    netflix_parse_precomputed(custIDAvgRating, 'extra/custIDAvgRatings.in')

    # Create dictionary of (decade, average rating) from precomputed file
    movieDecadeAvgRatings = {}
    netflix_parse_precomputed(movieDecadeAvgRatings, 'extra/movieDecadeAvgRatings.in')
    

    # Create {custID: {decade:average}} from precomputed file
    custDecadeAvgRatings = {}
    with open('extra/custDecadeAvgRatings.in', 'r') as f_myfile:
        lines = f_myfile.readlines()
        custID = ""
        for line in lines :
            if re.search(':', line) : #custID
                decadeAvgRating = {}
                custID = line.strip(':\r\n')
            else :
                assert custID
                decadeAvgRatingsList = line.strip().split('=')
                decade = decadeAvgRatingsList[0]
                average = decadeAvgRatingsList[1]
                decadeAvgRating[decade] = average
                custDecadeAvgRatings[custID] = decadeAvgRating
    
    # Parse training set data and probe data to find actual ratings
    movieIDDict = netflix_parse_train(trainingSetDir)
    actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
                           
    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    assert decadeAvgRating
    return [movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings]
    
# ------------
# netflix_eval
# ------------
#TODO: use arrays instead of lists?
def netflix_eval (probeFile, movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings) :
    """
    Applies heuristics to predict ratings and calculates the RMSE
    probeFile is the path to probe.txt from the command line
    movieIDAvgRating is the dictionary of {movie ID, average rating)
    custIDAvgRating is the dictionary of (cust ID, average rating)
    actualRatings is the list of actual customer ratings for RMSE calculation
    """
    
    movieIDpredRatings = {} # {movieID:[ratings]} for printing
    predRatings = []
    with open(probeFile, 'r') as f_myfile:
       lines = f_myfile.readlines()
       movieID = ""
       for line in lines :
            if re.search(':', line) : #movieID
               movieID = line.strip(':\r\n')
            else :
               assert movieID
               custID = line.strip() #strip newline
               
               #look up year
               year = movieIDYear[movieID]
            
               #determine the decade 
               decade = netflix_decade_calc(year)
               
               if decade in custDecadeAvgRatings[custID]:
                   custDecadeRating = float(custDecadeAvgRatings[custID][decade])
               else : #use individual customer average if customer didn't rate any movies in that decade
                   custDecadeRating =  float(custIDAvgRating[custID])
                
               pred = (float(movieIDAvgRating[movieID]) + float(custIDAvgRating[custID]) + float(movieDecadeAvgRatings[decade]) + custDecadeRating) / 4
               assert type(pred) is float
               predRatings.append(pred)
               movieIDpredRatings[movieID] = predRatings
                
    answer_rmse = rmse(actualRatings, predRatings)
    
    return [answer_rmse, movieDecadeAvgRatings]
        
# -------------
# netflix_solve
# -------------

def netflix_print (w, answer_rmse, movieIDpredRatings) :
    """
    Print the predicted results with RMSE at the top
    answer_rmse is the calculated RMSE
    movieIDpredRatings is the dictionary {movieID:[ratings]} for printing
    """
    assert answer_rmse 
    assert movieIDpredRatings
    
    w.write(str(round(answer_rmse, 3)) + "\n")
    for movieID in movieIDpredRatings :
        w.write(movieID + ":\n")
        predRatings = movieIDpredRatings[movieID]
        for pred in predRatings :
            w.write((str(round(pred,1))) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (w, trainingSetDir, probeFile) :
    """
    read, eval, print loop.
    w is a writer
    probeFile is the path to probe.txt from the command line
    trainingSetDir is the path to the training_set directory from the command line
    """
    assert trainingSetDir
    assert probeFile
    
    movieIDYear = {}
    movieDecadeAvgRatings = {}
    movieIDAvgRating = {}
    custDecadeAvgRatings = {}
    custIDAvgRating = {}
    actualRatings = []
    [movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings] = netflix_read(probeFile, trainingSetDir)
    
    assert movieIDYear
    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    assert movieDecadeAvgRatings
    assert custDecadeAvgRatings
    
    answer_rmse = 0.0
    movieIDpredRatings = {}
    [answer_rmse, movieIDpredRatings] = netflix_eval(probeFile, movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings)
    assert answer_rmse
    assert movieIDpredRatings
    
    netflix_print(w, answer_rmse, movieIDpredRatings)

# ----------
# Helpers
# ----------

def netflix_parse_precomputed(d, file, delimiter = "="):
    """
    Creates dictionary from precomputed file
    d is the dictionary of {first:second} i.e. {movie ID:average}
    file is the precomputed file with lines in the format first[delimiter]second i.e. movieID=average
    delimiter is the delimiter used to split each line
    return a dictionary of {first:second} i.e. {movie ID:average}
    """
    with open(file, 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines :
            list = line.strip().split(delimiter)
            first = list[0]
            second = list[1]
            d[first] = second
            
    return d

def netflix_actual_ratings(probeFile, movieIDDict):
    """
    Creates a list of actual ratings based on probe.txt for RMSE calculations
    probeFile is the path to probe.txt from the command line
    movieIDDict is a dictionary of dictionaries {movieID:{custID:rating}}
    return a list of actual ratings
    """
    assert probeFile
    assert movieIDDict

    actualRatingsList = []
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        movieID = ""
        for line in lines : 
            if re.search(':', line) : #movieID
                movieID = line.strip(':\r\n')
            else : #custID
                custID = line.strip()
                custIDRatingDict = movieIDDict[movieID]
                rating = custIDRatingDict[custID]
                actualRatingsList.append(rating)
    
    assert actualRatingsList
    return actualRatingsList

def netflix_parse_train (trainingSetDir):
    """
    Iterates through training_set/ and creates a dictionary of dictionaries to 
    facilitate actual rating look ups.  Used with netflix_actual_ratings.
    Assumes files in trainginSetDir are in the form mv_*.txt
    trainingSetDir is the path to the training_set directory from the command line
    return a dictionary of dictionaries {movieID:{custID:rating}}
    """
    
    assert trainingSetDir
    # Create dictionary of dictionaries {movieID:{custID:rating}}
    movieIDDict = {}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        #print file
        with open(file, 'r') as f_myfile:
            custIDRatingDict = {}
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            for custIDRatingDateLine in lines[1:] :
                custIDRatingDateList = custIDRatingDateLine.split(',')
                custID = custIDRatingDateList[0]
                rating = custIDRatingDateList[1].strip('\r\n')
                custIDRatingDict[custID] = rating
            assert custIDRatingDict
            movieIDDict[movieID] = custIDRatingDict

    assert movieIDDict
    return movieIDDict

def netflix_decade_calc (year):
    """
    Determine the decade given the year 
    year is a string from 1890 to 2005
    return the decade
    """
    assert '1890' <= year <= '2005' 
    decade = ""
    
    if '1890' <= year <= '1899' :
        decade = '1890s'
    elif '1900' <= year <= '1909':
        decade = '1900s'
    elif '1910' <= year <= '1919':
        decade = '1910s'
    elif '1920' <= year <= '1929':
        decade = '1920s'
    elif '1930' <= year <= '1939':
        decade = '1930s'
    elif '1940' <= year <= '1949':
        decade = '1940s'
    elif '1950' <= year <= '1959':
        decade = '1950s'
    elif '1960' <= year <= '1969':
        decade = '1960s'
    elif '1970' <= year <= '1979':
        decade = '1970s'
    elif '1980' <= year <= '1989':
        decade = '1980s'
    elif '1990' <= year <= '1999':
        decade = '1990s'
    elif '2000' <= year <= '2005':
        decade = '2000s'
    else :
        assert False #Should never reach this line. NULLs removed.
    
    assert decade
    return decade

# ----------------------------------------------------------
# Parsers for precomputed data
# These were ran once to generate precomputed files in extra/
# They will NOT be ran in normal execution
# ----------------------------------------------------------

def netflix_decade_avg (movieIDYear, trainingSetDir):
    """
    Compute customer averages per decade that the movie was created.
    Print to standard out or redirect to file using "> extra/movieIDAvgRatings.in"
    movieIDYear is the dictionary of (movie ID, year) created from extra/movieIDAvgRatings.in
    trainingSetDir is the path to training_set/ from the command line
    """
    assert trainingSetDir
    assert movieIDYear
    
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
    assert trainingSetDir
    # Compute average ratings for each movie, store in dict {movieID:Avg}
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
        



