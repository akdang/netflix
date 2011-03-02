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
import sys, os, glob, re


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
    
    #print len(movieIDAvgRating)
    assert movieIDAvgRating
    assert custIDAvgRating
    return [movieIDAvgRating, custIDAvgRating]

# ------------
# netflix_eval
# ------------

def netflix_eval (w, movieIDAvgRating, custIDAvgRating, probeFile) :
    """
    Attempts to match the men with the women such that if a man m
    prefers some woman w more than his wife, then w likes her 
    fiance more than m
    womenPrefs is a dictionary of (women, array of preferences) pairs
    menPrefs is a dictionary of (men, array of preferences) pairs
    return the engaged (men, women) pairs
    """
    
    predList = []
    # Iterate through probe file and make predictions
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        movieID = ""
        for line in lines :
            # Look for movieID
            if re.search(':', line) :
                movieID = line.strip(':\r\n')
                #print movieID
            else :
                assert movieID
                #custID = line.strip()
                pred = movieIDAvgRating[movieID]
                predList.append(pred)
                #print pred
    #print len(predList)  #1408395

    predList2 = []
    # Iterate through probe file and make predictions
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        movieID = ""
        for line in lines :
            # Look for movieID
            if re.search(':', line) :
                movieID = line.strip(':\r\n')
                #print movieID
            else :
                assert movieID
                custID = line.strip()
                pred = custIDAvgRating[custID]
                predList2.append(pred)
                #print pred
    #print len(predList2)  #1408395

    predList3 = []
    # Iterate through probe file and make predictions
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        movieID = ""
        for line in lines :
            # Look for movieID
            if re.search(':', line) :
                movieID = line.strip(':\r\n')
                #print movieID
            else :
                assert movieID
                custID = line.strip()
                pred = (float(movieIDAvgRating[movieID]) + float(custIDAvgRating[custID])) / 2
                assert type(pred) == float
		predList3.append(pred)
    #print len(predList2)  #1408395

    from RMSE import rmse
    print rmse(predList, predList3)
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
    custIDAvgRating = {}
    [movieIDAvgRating, custIDAvgRating] = netflix_read(r, trainingSetDir)
    assert movieIDAvgRating
    assert custIDAvgRating
    #netflix_movie_avg(trainingSetDir)
    netflix_eval(w, movieIDAvgRating, custIDAvgRating, probeFile)
    #netflix_actual(probeFile, trainingSetDir)
    #netflix_cust_avg(trainingSetDir)
    
# ----------------------------
# parsers for precomputed data
# ----------------------------

def netflix_movie_avg (trainingSetDir):
    assert trainingSetDir
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
        
def netflix_actual(probeFile, trainingSetDir):
    assert probeFile
    assert trainingSetDir

#    actualList = []
    index = 0
    out = open('extra/probeActualRatings.out', 'w')
    #for file in glob.glob(os.path.join('extra/probeFiles/', 'probe_*.txt')) :
    with open(probeFile, 'r') as f_myfile:
        lines = f_myfile.readlines()
        # in probeFile
        for line in lines : #movieID
            if re.search(':', line) :
                movieID = line.strip(':\n')
                trainingFile = "mv_%07d.txt" % int(movieID)
                out.write(line)
                print movieID
            else : #custID
                #assert movieID
                #assert trainingFile
                custID = line.strip()
                
                # In mv_trainingFile
                with open(os.path.join(trainingSetDir, trainingFile), 'r') as f_myfile:
                    lines = f_myfile.readlines()
                    #assert lines[0].strip(':\r\n') == movieID
                    for custIDRatingDateLine in lines[1:] :
                        custIDRatingDateList = custIDRatingDateLine.split(',')
                        if custID == custIDRatingDateList[0] :
                            rating = custIDRatingDateList[1]
                            out.write(rating + '\n')
                            #actualList.append(rating) #rating
                            break
                        else :
                            continue
    #print len(actualList)




