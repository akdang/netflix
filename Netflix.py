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
import sys, os, glob, re, time


# ------------
# netflix_read
# ------------

def netflix_read (r, probeFile, trainingSetDir) :
    """
    reads the input and parses it into preference dictionaries
    r is a reader
    numCouples is the number of couples
    isWomen indicates if we're iterating over women input
    return a list of [dict (person, array of preferences) pairs, and dict women ranks]
    """
	
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

# ------------
# netflix_eval
# ------------

def netflix_eval (w, probeFile, movieIDAvgRating, custIDAvgRating, actualRatings) :
    """
    Attempts to match the men with the women such that if a man m
    prefers some woman w more than his wife, then w likes her 
    fiance more than m
    womenPrefs is a dictionary of (women, array of preferences) pairs
    menPrefs is a dictionary of (men, array of preferences) pairs
    return the engaged (men, women) pairs
    """
    
#    movieAvgPreds = []
#    # Make predictions based on average rating of movie
#    # RMSE = 1.0519
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
#    # RMSE = 1.0426
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

    
    # Make predictions based on weighted averaged of movie and customer average ratings
    # RMSE = 1.0033
    movieCustAvgPreds = []
    with open('RunNetflix.out', 'w') as out: #print to output file
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
			   custID = line.strip()
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

def netflix_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    s = time.clock()
    
    if len(sys.argv) != 4 : 
        exit("Usage: python RunNetflix.py <movie titles file> <training set directory> <probe file>")
    else :
        movieTitlesFile = sys.argv[1]
        trainingSetDir = sys.argv[2]
        probeFile = sys.argv[3]
    
    movieIDAvgRating = {}
    custIDAvgRating = {}
    actualRatings = []
    movieIDDict = {}
    [movieIDAvgRating, custIDAvgRating, actualRatings] = netflix_read(r, probeFile, trainingSetDir)

    assert movieIDAvgRating
    assert custIDAvgRating
    assert actualRatings
    
    netflix_eval(w, probeFile, movieIDAvgRating, custIDAvgRating, actualRatings)
    #netflix_movie_avg(trainingSetDir)
    #netflix_cust_avg(trainingSetDir)
    
    e = time.clock()
    print (e - s), "seconds"
    
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
        
def netflix_actual_ratings(probeFile, movieIDDict):
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
    assert trainingSetDir
    # Create dictionary of dictionary {movieID:{custID:rating}}
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



