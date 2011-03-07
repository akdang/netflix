CS 373 Project 3: Netflix
Anh-Khoi Dang
ADD562

No additional, external modules used.

The parsers can be found in extra/Parsers.py

To use them:
1) from Parsers import netflix_decade_avg, netflix_movie_avg, netflix_cust_avg

netflix_decade_avg: Compute customer averages per decade that the movie was created.
netflix_movie_avg: Compute average rating for each movie
netflix_cust_avg: Compute average rating for each customer

2) call the appropriate function with the directory of the mv_*.txt
files. The optional second parameter is the output stream. The default
is sys.stdout.
Example: netflix_cust_avg('yourpath/to/training_set/')

3) Each parser will generate output delimited with the equal sign =. Be sure to redirect to file using "> extra/custIDAvgRatings.in"
Example (from custIDAvgRatings.in): 
(custID=average)
378466=4.45155393053
378467=3.48604651163
378465=3.91919191919
287141=3.78378378378
