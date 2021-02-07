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

def convert_date_time_to_epoch_time(time_to_convert):
    """
    """
    day = int(time_to_convert[3:5])
    year = int("20" + time_to_convert[6:])
    month = int(time_to_convert[0:2])

    epoch_time = datetime.datetime(year, month, day, 0, 0).strftime("%s")

    return epoch_time

def compute_all_words_of_given_time_period():
    pass

def compute_selected_word_of_given_time_period():
    pass

def compute_word_prevalence(user_input):
    """
    Inputs:
        user_input (dictionary): The user input is a dictionary
        of the following form {"time frame": (start_date, end_date),
        "data points": integer, "college" : [list of strings]}

        The start_date and end_date entered as input for "time_frame"
        will be in the following form: MM/DD/YY
    """
    pass

def create_graph():
    pass