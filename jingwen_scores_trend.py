"""
Reference (website)
"""

import csv
import time
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# This task is to analyze scores of each reddit post, 
# with the end goal to generate a graph that shows the
# best time to post in a given subreddit group to get
# more traffic.

# !!question: is epoch time a float, integer, or string?
# !!question: why is college in user_input a list of string?

# reminder of what the user_input dict looks like
'''
user_input (dictionary): The user input is a dictionary
        of the following form {"time frame": (start_date, end_date),
        "data points": integer, "college" : [list of strings],
        "word" : string}
'''

# 1. create time blocks and days - global variables
TIME_BLOCKS = list(range(0, 24))
DAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# DAY_TO_TIME = {}
# for day in DAY:
#     DAY_TO_TIME[day] = {}
#     for time in TIME_BLOCKS:
#         DAY_TO_TIME[day][time] = []


# 2. input a school name --> go to the corresponding csv

def get_csv(college):
    '''
    For a given college name input, return the desired csv file

    Input:
      college (string): college name

    Returns:
      csv_name (string): the name of the csv file
    '''
    return college + '_raw_data.csv'


# 3. convert epoch time into normal time

def epoch_to_day_time(epoch_time):
    '''
    For a given epoch time, return the corresponding
    time block and day

    Input:
      epoch_time (float): epoch time of a reddit post

    Returns:
      (time_block, day): time_block - integer
                         day - string
    '''
    standard_string = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(float(epoch_time)))
    # sample output: 'Sun, 14 Feb 2021 20:26:42 +0000'
    day = standard_string[:3]
    standard_time = re.findall('(\d\d)(:\d\d)(:\d\d)', standard_string)
    hour = int(standard_time[0][0])

    return (hour, day)


# 4. extract score, time, day information; create dictionary

def day_to_time_to_scores(csv_name):
    '''
    For a given csv file, extract the score and time information of each post
    Assign posts to their corresponding time block
    Calculate the averaged score of each time block of each day

    Input:
      csv_name (string): name of the csv file

    Returns:
      day_to_time_to_scores (dict): a dictionary that maps each day to its 24
                                    time blocks; each time block maps to a list 
                                    of post scores and an integer representing 
                                    the average
    '''
    rv = {}

    with open(csv_name) as f:
        reader = csv.DictReader(f)
        for row in reader:
            epoch_time = row['epoch_time']
            hour, day = epoch_to_day_time(epoch_time)
            if day not in rv:
                rv[day] = {}
            if hour not in rv[day]:
                rv[day][hour] = {}
                rv[day][hour]['scores'] = []
            rv[day][hour]['scores'].append(row['score'])

    return rv


# 5. prepare an array for graphing

def get_array(day_time_scores):
    '''
    Get a numpy array of averaged scores in a 7x24 matrix

    Input:
      day_time_scores (dict): the dictionary that maps time to scores
    
    Returns:
      a numpy array whose row numbers should be equal to the number
      of days, and column numbers should be equal to the number of hours
    '''
    day_averages = []

    for day in day_time_scores:
        hour_averages = []
        for hour in day_time_scores[day]:
            scores = day_time_scores[day][hour][scores]
            hour_average = sum(scores) / len(scores)
            hour_averages.append(hour_average)
        day_averages.append(hour_averages)

    averages = np.array(day_averages)

    return averages


# 6. plot the graph (preferably using different shades of the school's color?)
# Reference: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html

def graphing(averages):
    '''
    Given a dictionary of time and scores, plot a heatmap

    Input:
      averages (numpy array)

    Returns:
      ??
    '''
    fig, ax = plt.subplots()
    im = ax.imshow(averages)

    ax.set_xticks(np.arange(len(TIME_BLOCKS)))
    ax.set_yticks(np.arange(len(DAY)))

    ax.set_xticklabels(TIME_BLOCKS)
    ax.set_yticklabels(DAY)

    for i in range(len(DAY)):
        for j in range(len(TIME_BLOCKS)):
            text = ax.text(j, i, averages[i, j],
                           ha="center", va="center", color="w")

    ax.set_title("When is the best time to post?")
    fig.tight_layout()
    plt.show()


def main(user_input):
    '''
    Main function

    Input: 
      user_input (dictionary): The user input is a dictionary
      of the following form {"time frame": (start_date, end_date),
      "data points": integer, "college" : [list of strings],
      "word" : string}
    
    Returns:
      a heatmap that shows which time period gains the most traffic
    '''
    college_name = user_input['college']
    csv_name = get_csv(college_name)
    day_time_scores = day_to_time_to_scores(csv_name)
    averages = get_array(day_time_scores)
    return averages
    graphing(averages)
    # do I need to return anything here?