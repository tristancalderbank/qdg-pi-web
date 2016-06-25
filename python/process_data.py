#!/usr/bin/env python
import cgi
#import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

# QDG Pi Project
# Quantum Degenerate Gases Lab (Madison Research Group)
# publish_data.py
# date: May 27, 2016
# author: tristan calderbank
# contact: tristan@alumni.ubc.ca
# purpose: This script contains functions to process the
#          sensor data, and calculate the appropriate stats
#          
# arguements: room name (master or mol), sensor number (0-7)

import csv
import sys
import os
from itertools import islice
import numpy
import time
import datetime
import math
import os.path
import fcntl
# constants

SHORT_TERM_TIME = 60 * 60 * 24 # 24 hours in seconds

# csv column indexes
DATE = 0
TEMPERATURE = 1
PRESSURE = 2
HUMIDITY = 3

MAX = 0
MIN = 1
MEAN = 2
STD = 3

LONGTERM_OFFSET = 2
NUMBER_OF_STAT_COLUMNS = 4
SAMPLE_SIZE = 1

#------------------------------------------------#
# get_sorted_file_list()                         #
#                                                #
# Given a directory returns a sorted list of csv #
# files in that directory                        #
#                                                #
#------------------------------------------------#
def get_sorted_file_list(path):
        
    list = os.listdir(path)
    csv_list = []

    for file in list:
        if file.endswith('.csv'):
            csv_list.append(file)

    csv_list = sorted(csv_list)
    return csv_list

#------------------------------------------------#
# condense_file()                                #
#                                                #
# Creates a shortened file by only keeping every #
# Nth line from the input file                   #
#                                                #
# parameters:                                    #
#                                                #
# cutoff - number of lines at which to stop      #
# writing                                        #
#                                                #
# total_rows - running total of rows written     #
#                                                #
#------------------------------------------------#
def condense_file(input_file, output_file, N, total_rows, cutoff):

    input_file_csv = csv.reader(input_file, delimiter=',')
    row_number = 0

    for row in input_file_csv:

        if((total_rows + row_number) == cutoff):
            return row_number

        if(row_number % N == 0):
            output_file.writerow(row)

        row_number+=1
    return row_number

#------------------------------------------------#
# csv_file_to_matrix()                           #
#                                                #
# Given a path to a csv file, returns a numpy    #
# matrix                                         #
#                                                #
#------------------------------------------------#
def csv_file_to_matrix(input_path):

    with open(input_path, 'r') as input_file:

        fcntl.flock(input_file, fcntl.LOCK_EX)

        input_file_csv = csv.reader(input_file, delimiter=',')
        matrix = numpy.array(list(input_file_csv))

        fcntl.flock(input_file, fcntl.LOCK_UN)

    return matrix

#------------------------------------------------#
# date_to_unix_stamp()                           #
#                                                #
# Given a date in the specified format, returns  #
# a unix timestamp for that date                 #
#                                                #
#------------------------------------------------#
def date_to_unix_stamp(date):
    return time.mktime(time.strptime(date, "%Y-%m-%d"))

#------------------------------------------------#
# get_stats()                                    #
#                                                #
# Given a matrix and a column, returns an array  #
# with max, min, mean, and std                   #
#                                                #
#------------------------------------------------#
def get_stats(matrix, column):

    matrix = matrix[:, column].astype(float)

    max = round(numpy.max(matrix), 2)
    min = round(numpy.min(matrix), 2)
    mean = round(numpy.mean(matrix), 2)
    std = round(numpy.std(matrix), 2)

    return [max, min, mean, std]


#------------------------------------------------#
# get_stats_long()                               #
#                                                #
# Given a matrix of stats, calculates the meta   #
# stats of that matrix                           #
#                                                #
#------------------------------------------------#
def get_stats_long(matrix, column):


    max = round(numpy.max(matrix[:, column + MAX].astype(float)), 2)
    min = round(numpy.min(matrix[:, column + MIN].astype(float)), 2)
    mean = round(numpy.mean(matrix[:, column + MEAN].astype(float)), 2)

    std = matrix[:, column + STD].astype(float)
    sample_size = matrix[:, SAMPLE_SIZE].astype(float)

    sum_of_squares = 0

    for i in range(0, len(std)):
        sum_of_squares = sum_of_squares + std[i]**2 / sample_size[i]

    std = round(math.sqrt(sum_of_squares), 2)

    return [max, min, mean, std]


#------------------------------------------------#
# process_stats_short_term()                     #
#                                                #
# Creates a csv file with stats for each of      #
# temperature, pressure, and humidity            #
#                                                #
#------------------------------------------------#
def process_stats_short_term(input_file, output_file):

    if(os.path.isfile(input_file) == True):

        with open(output_file, 'w') as output_file:
            output_file_csv = csv.writer(output_file, delimiter=',')
            with open(input_file, 'r') as input_file:
                input_file_csv = csv.reader(input_file, delimiter=',')

                data = numpy.array(list(input_file_csv))

                temperature_stats = get_stats(data, TEMPERATURE)
                pressure_stats = get_stats(data, PRESSURE)
                humidity_stats = get_stats(data, HUMIDITY)

            output_file_csv.writerow(temperature_stats)
            output_file_csv.writerow(pressure_stats)
            output_file_csv.writerow(humidity_stats)


#------------------------------------------------#
# process_stats_long_term()                      #
#                                                #
# Gets all time stats for the daily long term    #
# data                                           #
#                                                #
#------------------------------------------------#
def process_stats_long_term(input_file, output_file):

    if(os.path.isfile(input_file) == True):

        with open(output_file, 'w') as output_file:
            output_file_csv = csv.writer(output_file, delimiter=',')
            with open(input_file, 'r') as input_file:
                input_file_csv = csv.reader(input_file, delimiter=',')

                data = numpy.array(list(input_file_csv))

                temperature_stats = get_stats_long(data, LONGTERM_OFFSET + (TEMPERATURE - 1)*NUMBER_OF_STAT_COLUMNS)
                pressure_stats = get_stats_long(data, LONGTERM_OFFSET + (PRESSURE - 1)*NUMBER_OF_STAT_COLUMNS)
                humidity_stats = get_stats_long(data, LONGTERM_OFFSET + (HUMIDITY - 1)*NUMBER_OF_STAT_COLUMNS)

            output_file_csv.writerow(temperature_stats)
            output_file_csv.writerow(pressure_stats)
            output_file_csv.writerow(humidity_stats)

#------------------------------------------------#
# process_short_term()                           #
#                                                #
# Concatenates all csv files in a directory to   #
# an output file                                 #
#                                                #
# optional parameters:                           #
#                                                #
# 'N' keeps only Nth lines from every file       #
# 'days' keeps the last X days, 0 for all        #
#                                                #
#------------------------------------------------#
def process_short_term(directory, output_path, N=1):


    file_list = get_sorted_file_list(directory)
    number_of_days = len(file_list)

    if(number_of_days == 0):
        print "Looks like there's no data to process..."
        return

    row_number = 0
    most_recent_timestamp = get_latest_timestamp(directory, file_list[-1])

    # to get 24 hours of data, only need last two days at most
    if number_of_days > 1:
        file_list = file_list[-2:]

    with open(output_path, 'w') as output_file:

        output_file_csv = csv.writer(output_file)
        start_writing = False

        for file in file_list:

            file_path = directory + '/' + file

            with open(file_path, 'r') as current_file:

                input_file_csv = csv.reader(current_file, delimiter=',')
                for row in input_file_csv:

                    current_timestamp = date_string_to_unix_stamp(row[0])

                    if number_of_days == 1:
                        start_writing = True

                    if number_of_days > 1 and (most_recent_timestamp - current_timestamp) < SHORT_TERM_TIME:
                        start_writing = True

                    if(row_number % N == 0) and start_writing == True:
                        row[0] = str(time.mktime(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").timetuple()))
                        output_file_csv.writerow(row)
                        row_number +=1

    print "Processed " + str(row_number) + " rows of data sucessfully."


#------------------------------------------------#
# get_latest_timestamp()                         #
#                                                #
# opens the latest data file and grabs the last  #
# timestamp                                      #
#                                                #
#------------------------------------------------#

def get_latest_timestamp(directory, file):

    file_path = directory + '/' + file

    with open(file_path, 'r') as current_file:

        input_file_csv = csv.reader(current_file, delimiter=',')
        file_as_list = list(input_file_csv)
        most_recent_timestamp = date_string_to_unix_stamp(file_as_list[-1][0])

    return most_recent_timestamp

#------------------------------------------------#
# date_string_to_unix_stamp()                    #
#                                                #
# returns a integer in unix epoch time from a    #
# given date string                              #
#------------------------------------------------#

def date_string_to_unix_stamp(string):
    return time.mktime(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").timetuple())

#------------------------------------------------#
# process_long_term()                            #
#                                                #
# Creates or adds to a long term file with       #
# one row for each day, using csv files from a   #
# given directory                                #
#                                                #
#------------------------------------------------#
def process_long_term(directory, output_path):
    
    file_list = get_sorted_file_list(directory)

    if len(file_list) == 0:
        return

    # create output file if it doesn't exist
    if not os.path.exists(output_path):
        open(output_path, 'w').close()

    # previous days is a list of days already in the long term data file
    previous_days = []

    if os.path.getsize(output_path) > 0: 
        previous_file = csv_file_to_matrix(output_path)
        previous_days = previous_file[:,0].astype(float)

    with open(output_path, 'r+') as output_file:

        number_processed = 0

        output_file_csv = csv.writer(output_file, delimiter=',')

        for file in file_list:

            current_file_date = date_to_unix_stamp(file.split('.', 1)[0])

            # the stats for the current day will have changed so first delete the old entry for today (last line of file)
            if (previous_days != []) and (current_file_date == previous_days[-1]):
                rows = output_file.readlines() 
                del rows[-1]
                output_file.seek(0, 0)
                output_file.writelines(rows)
                previous_days = previous_days[0:-1]

            # check that the previous data isn't empty and don't recalculate data for old days
            if (previous_days == []) or (current_file_date not in previous_days):

                file_path = directory + '/' + file

                current_file_matrix = csv_file_to_matrix(file_path)

                # get the number of rows in the file as its needed to calculate total std later

                with open(file_path, 'r') as current_file:

                    fcntl.flock(current_file, fcntl.LOCK_EX)

                    current_file_num_rows = len(current_file.readlines())

                    fcntl.flock(current_file, fcntl.LOCK_UN)

                unix_date = date_to_unix_stamp(file.split('.', 1)[0])

                stats = [unix_date] + [current_file_num_rows] + get_stats(current_file_matrix, TEMPERATURE)
                stats = stats + get_stats(current_file_matrix, PRESSURE) + get_stats(current_file_matrix, HUMIDITY)
                output_file_csv.writerow(stats)


                number_processed+=1

# Main program

#room_name = str(sys.argv[1])
#sensor_number = str(sys.argv[2])
#short_or_long_term = str(sys.argv[3])


arguments = cgi.FieldStorage()

room_name = str(arguments["room"].value)
sensor_number = str(arguments["sensor"].value)
short_or_long_term = str(arguments["longshort"].value)

data_directory = '/var/www/qdg-pi-web/data/'
input_directory = data_directory + room_name + "/sensor_" + sensor_number
output_directory = '/var/www/qdg-pi-web/data/page-data/'
times_run = 0

#while True:

if(short_or_long_term == 'short'):
    # process short stuff
    output_path = output_directory + room_name + '-sensor-' + sensor_number + '-short.csv'
    output_path_stats = output_directory + room_name + '-sensor-' + sensor_number + '-short-stats.csv'

    process_short_term(input_directory, output_path, 1)
    process_stats_short_term(output_path, output_path_stats) 


elif (short_or_long_term == 'long'):
    # process long term stuff
    output_path = output_directory + room_name + '-sensor-' + sensor_number + '-long.csv'
    output_path_stats = output_directory + room_name + '-sensor-' + sensor_number + '-long-stats.csv'

    process_long_term(input_directory, output_path)
    process_stats_long_term(output_path, output_path_stats)

#    times_run +=1
#    print times_run










