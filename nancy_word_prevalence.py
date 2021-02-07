"""
References: https://docs.python.org/3/library/time.html#time.strftime
"""

# This task is to analyze word prevalence over time

# It will create a graph that will show word prevalence
# as a percentage of total words over time

# The user will input the time frame, how many
# data points they would like from that time period,
# and which college they would like to see (this can
# be more than one college, and if
# they enter nothing for college, it will compute
# the word prevalence across the entire dataset)

# For instance, if the time frame is 5 years, and the user
# wants 5 data points, then the graph generated will have
# a data point for every year, and the duration for which
# the word will be calculated will be a year.

import datetime
import sqlite3


def convert_date_time_to_epoch_time(time_to_convert):
    """
    This function uses the datetime package to convert date time
    to epoch time.

    Inputs:
        time_to_convert (string): in the form "MM/DD/YY"
    
    Outputs:
        epoch_time (string): string of the time in epoch time
    """
    day = int(time_to_convert[3:5])
    year = int("20" + time_to_convert[6:])
    month = int(time_to_convert[0:2])

    epoch_time = datetime.datetime(year, month, day, 0, 0).strftime("%s")

    return epoch_time

def compute_all_words_of_given_time_period(start_epoch_date, end_epoch_date, colleges):
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = ("""SELECT count(*) FROM post_words JOIN post_info
                 ON post_words.unique_post_id = post_info.unique_post_id
                  WHERE post_info.epoch_time >= ? AND post_info.epoch_time <= ?""")

    params = [start_epoch_date, end_epoch_date]

    if colleges != []:
        for college in colleges:
            params.append(college)
            if college == colleges[0]:
                query += " AND (post_info.subreddit = ? COLLATE NOCASE "
            if college == colleges[-1]:
                query += ")"
            else:
                query += " OR post_info.subreddit = ? COLLATE NOCASE"
    params = tuple(params)
    
    r = c.execute(query, params)
    word_count_all = r.fetchall()
    word_count_all = word_count_all[0][0]
    db.close()
    return word_count_all

def compute_selected_word_of_given_time_period(start_epoch_date, end_epoch_date, colleges, word):
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = ("""SELECT count(*) FROM post_words JOIN post_info
                 ON post_words.unique_post_id = post_info.unique_post_id
                  WHERE post_info.epoch_time >= ? AND post_info.epoch_time <= ?
                   AND post_words.word = ? COLLATE NOCASE""")
    
    params = [start_epoch_date, end_epoch_date, word]

    if colleges != []:
        for college in colleges:
            params.append(college)
            if college == colleges[0]:
                query += " AND (post_info.subreddit = ? COLLATE NOCASE "
            if college == colleges[-1]:
                query += ")"
            else:
                query += " OR post_info.subreddit = ? COLLATE NOCASE"
    
    params = tuple(params)
    r = c.execute(query, params)
    word_count = r.fetchall()
    word_count = word_count[0][0]
    db.close()
    return word_count
    
    

def compute_word_as_percentage_of_all_words(start_epoch_time, end_epoch_time, colleges, word):

    word_count_all = compute_all_words_of_given_time_period(start_epoch_time, end_epoch_time, colleges)
    word_count = compute_selected_word_of_given_time_period(start_epoch_time, end_epoch_time, colleges, word)
    if word_count_all == 0:
        word_percentage = 0
    else:
        word_percentage = (word_count/word_count_all) * 100
    return word_percentage


def compute_epoch_times(epoch_start_date, epoch_end_date, data_points):
    """
    Inputs:
        epoch_start_date (string): start date in terms of epoch time
        epoch_end_date (string): end date in terms of epoch time
        data_points(integer): amount of desired datapoints
    
    Outputs:
        data_point_times: list of integers representing epoch times to
                          create intervals to compute
    """
    difference = int(epoch_end_date) - int(epoch_start_date)
    difference_between_datapoints = difference / data_points

    next_date = int(epoch_start_date) + difference_between_datapoints
    data_point_times = [int(epoch_start_date), next_date]

    for i in range(data_points - 2):
        next_date = next_date + difference_between_datapoints
        data_point_times.append(next_date)
    
    return data_point_times


def compute_word_prevalence(user_input):

    """
    Inputs:
        user_input (dictionary): The user input is a dictionary
        of the following form {"time frame": (start_date, end_date),
        "data points": integer, "college" : [list of strings],
        "word" : string}

        The start_date and end_date entered as input for "time_frame"
        will be in the following form: MM/DD/YY
    """

    start_date, end_date = user_input["time frame"]
    epoch_start_date = convert_date_time_to_epoch_time(start_date)
    epoch_end_date = convert_date_time_to_epoch_time(end_date)

    data_points = user_input["data points"]
    data_point_times = compute_epoch_times(epoch_start_date, epoch_end_date, data_points)

    i = 0
    # contains range of indexes
    range_of_times = []

    for i in range(data_points - 1):
        range_of_one_time = (i, i+1)
        range_of_times.append(range_of_one_time)
    
    word_percentages = []
    colleges = []
    if "college" in user_input:
        colleges = user_input["college"]
    for range_of_one_time in range_of_times:
        starting_index, ending_index = range_of_one_time
        if range_of_one_time != range_of_times[-1]:
            data_point_time = tuple(data_point_times[starting_index: ending_index + 1])
        else:
            data_point_time = tuple(data_point_times[starting_index:])
        starting_index, ending_index = data_point_time
        word_percentage = compute_word_as_percentage_of_all_words(starting_index, ending_index, colleges, user_input["word"])
        word_percentages.append(word_percentage)

    return word_percentages



def create_graph():
    pass
