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
    
    # Parse training set data and probe data to find actual ratings
    movieIDDict = netflix_parse_train(trainingSetDir)
    actualRatings = netflix_actual_ratings(probeFile, movieIDDict)
                           
    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    return [movieIDAvgRating, custIDAvgRating, actualRatings]
    
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
    
    #print "actualRatingsList length: ", len(actualRatingsList)
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
    #print "movieIDDict length:", len(movieIDDict)    
    assert movieIDDict
    return movieIDDict

# ------------
# netflix_eval
# ------------
#TODO: use arrays instead of lists?
def netflix_eval (probeFile, movieIDAvgRating, custIDAvgRating, actualRatings) :
    """
    Applies heuristics to predict ratings and calculates the RMSE
    Prints result to file specified in fileOutput variable
    probeFile is the path to probe.txt from the command line
    movieIDAvgRating is the dictionary of {movie ID, average rating)
    custIDAvgRating is the dictionary of (cust ID, average rating)
    actualRatings is the list of actual customer ratings for RMSE calculation
    """
    
#    movieAvgPreds = []
#    # Make predictions based on average rating of movie
#    # RMSE = 1.052
#    with open(probeFile, 'r') as f_myfile:
#        lines = f_myfile.readlines()
#        movieID = ""
#        for line in lines :
#            if re.search(':', line) :
#                movieID = line.strip(':\r\n')
#            else :
#                assert movieID
#                pred = movieIDAvgRating[movieID]
#                movieAvgPreds.append(pred)
#
#    print rmse(actualRatings, movieAvgPreds)
#
#    custAvgPreds = []
#    # Make predictions based on average rating of customer
#    # RMSE = 1.043
#    with open(probeFile, 'r') as f_myfile:
#        lines = f_myfile.readlines()
#        for line in lines :
#            if re.search(':', line) :
#                continue
#            else :
#                custID = line.strip()
#                pred = custIDAvgRating[custID]
#                 custAvgPreds.append(pred)
#
#    print rmse(actualRatings, custAvgPreds)

    fileOutput = 'RunNetflix.out' #Change this for output file
    # Make predictions based on average of movie and customer average ratings
    # RMSE = 1.003
    movieCustAvgPreds = []
    with open(fileOutput, 'w') as out: #print to output file
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
			   pred = (float(movieIDAvgRating[movieID]) + float(custIDAvgRating[custID])) / 2
			   assert type(pred) is float
			   movieCustAvgPreds.append(pred)
			   out.write(str(round(pred, 1)) + "\n")
                
    answer_rmse = rmse(actualRatings, movieCustAvgPreds)
    with open('RunNetflix.out', 'r+') as out:
	 out.write(str(round(answer_rmse, 3)) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (movieTitlesFile, trainingSetDir, probeFile) :
    """
    read, eval, print loop.
    movieTitlesFile is the path to movie_titles.txt from the command line
    probeFile is the path to probe.txt from the command line
    trainingSetDir is the path to the training_set directory from the command line
    """
    
    movieIDAvgRating = {}
    custIDAvgRating = {}
    actualRatings = []
    movieIDDict = {}
    [movieIDAvgRating, custIDAvgRating, actualRatings] = netflix_read(probeFile, trainingSetDir)

    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    
    netflix_eval(probeFile, movieIDAvgRating, custIDAvgRating, actualRatings)
    #netflix_movie_avg(trainingSetDir)
    #netflix_cust_avg(trainingSetDir)
    
    
# ----------------------------
# parsers for precomputed data
# ----------------------------

def netflix_movie_avg (trainingSetDir):
    assert trainingSetDir
    # Compute average ratings for each movie, store in dict {movieID:Avg}
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
    
def netflix_cust_avg (trainingSetDir) :
    assert trainingSetDir
    # Compute customer averages using dictionary of list {custID: [totalRating, numRatings]}
    custIDTotalRatingDict = {}
    for file in glob.glob(os.path.join(trainingSetDir, 'mv_*.txt')) :
        with open(file, 'r') as f_myfile:
            lines = f_myfile.readlines()
            movieID = lines[0].strip(':\r\n')
            for custIDRatingDateLine in lines[1:] :
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
                
    #custIDAvgDict = {}
    # compute averages for each computer. store in dict {custID:Avg}
    for custID in custIDTotalRatingDict :
        totalRatingNumRatingList = custIDTotalRatingDict[custID]
        totalRating = totalRatingNumRatingList[0]
        numRating = totalRatingNumRatingList[1]
        avgRating = totalRating / numRating
        #custIDAvgDict[custID] = avgRating
        print custID + "=" + str(avgRating)
        



