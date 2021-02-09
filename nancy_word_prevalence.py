"""
References: https://docs.python.org/3/library/time.html#time.strftime
            https://realpython.com/python-matplotlib-guide/
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
import matplotlib.pyplot as plt

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

def convert_epoch_time_to_date_time(times_to_convert):
    """
    This function takes in a list of tuples of epoch times
    and converts the values into date time format.

    Inputs:
        times_to_convert (list of tuples of integers): represents
        the intervals of time
    Outputs:
        converted_times (list of tuples of integers): represents
        the intervals of time in date time format.
    """
    converted_times = []
    single_time = []
    for time1 in times_to_convert:
        start_time, end_time = time1
        for time2 in time1:
            converted_time = datetime.datetime.fromtimestamp(time2).strftime("%m/%d/%Y")
            single_time.append(converted_time)
        single_time = str(tuple(single_time))
        converted_times.append(single_time)
        single_time = []
    
    return converted_times
        

def compute_all_words_of_given_time_period(start_epoch_date, end_epoch_date, colleges):
    """
    This functions returns back the number of words from a given time period.

    Inputs:
        start_epoch_date (int): start time in epoch units
        end_epoch_date (int): end time in epoch units
        colleges (list of strings): list of names of colleges

    Outputs:
        word_count_all (int): the number of words from the given time period
    """
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
    """
    This functions returns back the number of times
    a given word was used during a given time period.

    Inputs:
        start_epoch_date (int): start time in epoch units
        end_epoch_date (int): end time in epoch units
        colleges (list of strings): list of names of colleges
        word (string): word to search for

    Outputs:
        word_count (int): the amount of times the word appears in the time period
    """
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
    
    

def compute_word_as_percentage_of_all_words(start_epoch_date, end_epoch_date, colleges, word):
    """
    Uses the compute_selected_word_of_given_time_period and
    the compute_all_words_given_time_period functions to compute
    the percentage of all words that the given word was used
    during the time period.

    Inputs:
        start_epoch_date (int): start time in epoch units
        end_epoch_date (int): end time in epoch units
        colleges (list of strings): list of names of colleges
        word (string): word to search for
    Outputs:
        word_percentage (float): percentage of all words that the given word
                                 was used during the time period.
    """

    word_count_all = compute_all_words_of_given_time_period(start_epoch_date, end_epoch_date, colleges)
    word_count = compute_selected_word_of_given_time_period(start_epoch_date, end_epoch_date, colleges, word)
    if word_count_all == 0:
        word_percentage = 0
    else:
        word_percentage = (word_count/word_count_all) * 100
    return word_percentage


def compute_epoch_times(epoch_start_date, epoch_end_date, data_points):
    """
    Segments the period of time between the start date and end date into
    enough components to equal the amount of desired data_points.

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

    for i in range(data_points - 1):
        next_date = next_date + difference_between_datapoints
        data_point_times.append(next_date)
    return data_point_times


def compute_word_prevalence(user_input):
    """
    Given the user input, the function compute the word prevalence across
    a given period of time, segmented into chunks.

    Inputs:
        user_input (dictionary): The user input is a dictionary
        of the following form {"time frame": (start_date, end_date),
        "data points": integer, "college" : [list of strings],
        "word" : string}

        The start_date and end_date entered as input for "time_frame"
        will be in the following form: MM/DD/YY
    Outputs:
        word_percentages (list of floats): percent of time that the word shows up
                                            in each of the time periods
        converted_times (list of strings): list of intervals of times
        user_input["word"] (string): desired word to return
    """

    start_date, end_date = user_input["time frame"]
    epoch_start_date = convert_date_time_to_epoch_time(start_date)
    epoch_end_date = convert_date_time_to_epoch_time(end_date)

    data_points = user_input["data points"]
    data_point_times = compute_epoch_times(epoch_start_date, epoch_end_date, data_points)

    i = 0
    # contains range of indexes
    range_of_times = []

    for i in range(data_points):
        range_of_one_time = (i, i+1)
        range_of_times.append(range_of_one_time)
    
    data_point_intervals = []
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
        data_point_intervals.append(data_point_time)
        starting_index, ending_index = data_point_time
        word_percentage = compute_word_as_percentage_of_all_words(starting_index, ending_index, colleges, user_input["word"])
        word_percentages.append(word_percentage)

    converted_times = convert_epoch_time_to_date_time(data_point_intervals)
    return (word_percentages, converted_times, user_input["word"])

def create_graph(user_input):
    """
    Takes in the user_input and returns a graph of the desired data.

    Inputs:
        user_input (dictionary): The user input is a dictionary
        of the following form {"time frame": (start_date, end_date),
        "data points": integer, "college" : [list of strings],
        "word" : string}

        The start_date and end_date entered as input for "time_frame"
        will be in the following form: MM/DD/YY
    
    Outputs:
        graphs
    """

    word_percentages, converted_times, word = compute_word_prevalence(user_input)
    x = converted_times
    y = word_percentages

    fig = plt.figure()
    plt.plot(x, y)

    plt.xticks(rotation = 90, fontsize = 10)

    plt.xlabel("time period (" + converted_times[0][2:10] +" to " + converted_times[-1][-12:-2] + ")")
    plt.ylabel("percentage use of word")

    plt.title("Percentage use of (" + word + ") over time")

    plt.tight_layout()
    
    plt.show()

    return fig

