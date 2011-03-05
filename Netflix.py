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
    
    # TODO: refactor into separate function
    # Create dictionary of (movie ID, average rating) from precomputed file
    movieIDAvgRating = {}
    with open('extra/movieIDAvgRatings.in', 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines :
            movieIDAvgRatingsList = line.strip().split('=')
            movieID = movieIDAvgRatingsList[0]
            average = movieIDAvgRatingsList[1]
            movieIDAvgRating[movieID] = average
    
    # Create dictionary of (cust ID, average rating) from precomputed file
    custIDAvgRating = {}
    with open('extra/custIDAvgRatings.in', 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines :
            custIDAvgRatingsList = line.strip().split('=')
            custID = custIDAvgRatingsList[0]
            average = custIDAvgRatingsList[1]
            custIDAvgRating[custID] = average
            
    # Create dictionary of (decade, average rating) from precomputed file
    movieDecadeAvgRatings = {}
    with open('extra/movieDecadeAvgRatings.in', 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines :
            decadeAvgRatingsList = line.strip().split('=')
            decade = decadeAvgRatingsList[0]
            average = decadeAvgRatingsList[1]
            movieDecadeAvgRatings[decade] = average
            
    # Create {custID: {decade:[totalRating, numRatings]}} from precomputed file
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

    # Create dictionary of (movie ID, year) from input file
    movieIDYear = {}
    with open('extra/movie_titles_no_nulls.txt', 'r') as f_myfile:
        lines = f_myfile.readlines()
        for line in lines: #movieID, year, title
            movieIDYearList = line.strip().split(',')
            movieID = movieIDYearList[0]
            year = movieIDYearList[1]
            movieIDYear[movieID] = year

    # Parse training set data and probe data to find actual ratings
    movieIDDict = netflix_parse_train(trainingSetDir)
    actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
                           
    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    assert decadeAvgRating
    return [movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings]
    
# --------------------------
# Helpers for netflix_read
# --------------------------

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
    facilitate actual rating look ups
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
                rating = custIDRatingDateList[1]
                custIDRatingDict[custID] = rating
            assert custIDRatingDict
            movieIDDict[movieID] = custIDRatingDict

    assert movieIDDict
    return movieIDDict

# ------------
# netflix_eval
# ------------
#TODO: use arrays instead of lists?
def netflix_eval (probeFile, movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings) :
    """
    Applies heuristics to predict ratings and calculates the RMSE
    Prints result to file specified in outputFile variable
    probeFile is the path to probe.txt from the command line
    movieIDAvgRating is the dictionary of {movie ID, average rating)
    custIDAvgRating is the dictionary of (cust ID, average rating)
    actualRatings is the list of actual customer ratings for RMSE calculation
    """
    
    outputFile = 'RunNetflix.out' #Change this for output file
    # Make predictions based on average of movie and customer average ratings
    # RMSE = 1.003
    movieCustAvgPreds = []
    with open(outputFile, 'w') as out: #print to output file
        out.write("0.000\n") #placeholder for RMSE at top of file
        with open(probeFile, 'r') as f_myfile:
           lines = f_myfile.readlines()
           movieID = ""
           for line in lines :
                if re.search(':', line) : #movieID
                   out.write(line) 
                   movieID = line.strip(':\r\n')
                else :
                   assert movieID
                   custID = line.strip() #strip newline
                   
                   #look up year
                   year = movieIDYear[movieID]
                
                   #determine the decade 
                   decade = netflix_decade_calc(year)
                   
                   pred = (float(movieIDAvgRating[movieID]) + float(custIDAvgRating[custID]) + float(decadeAvgRating[decade])) / 3
                   assert type(pred) is float
                   movieCustAvgPreds.append(pred)
                   out.write(str(round(pred, 1)) + "\n")
                
    answer_rmse = rmse(actualRatings, movieCustAvgPreds)
    with open(outputFile, 'r+') as out:
        out.write(str(round(answer_rmse, 3)) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (trainingSetDir, probeFile) :
    """
    read, eval, print loop.
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
    
    netflix_eval(probeFile, movieIDYear, custDecadeAvgRatings, movieDecadeAvgRatings, movieIDAvgRating, custIDAvgRating, actualRatings)
    
# ----------------------------
# parsers for precomputed data
# ----------------------------

def netflix_decade_calc (year):
    assert '1890' <= year <= '2005' 
    decade = ""
    #determine the decade 
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
    
    assert decade
    return decade

def netflix_decade_movie_avg (movieIDYear, trainingSetDir):
    assert trainingSetDir
    assert movieIDYear
    
    # Compute decade averages per customer using dict of dict of list {custID: {decade:[totalRating, numRatings]}}
    custIDDecade = {}
    decadeDict = {'1890s':[0, 0],'1900s':[0, 0],'1910s':[0, 0],'1920s':[0, 0],'1930s':[0, 0],'1940s':[0, 0],'1950s':[0, 0],'1960s':[0, 0],'1970s':[0, 0],'1980s':[0, 0],'1990s':[0, 0],'2000s':[0, 0]}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        #print file
        with open(file, 'r') as f_myfile:
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            for custIDRatingDateLine in lines[1:] :
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
            if totalRating == 0 :
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
        



