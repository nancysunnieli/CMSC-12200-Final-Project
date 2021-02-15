'''
This task is to return the top terms w/ the given parameters by the user being:
    1) the school name,
    2) the number of words you want to receive back (n-grams),
    3) the number of n-grams you want to see (k number of n-grams),
    4) the start and end time range you want to comb thru,
            (optional, assume all time otherwise)
    5) and the upote/downvote ratio (optional)
'''
import csv
# import UChicago_raw_data as uchicago
from evan_word_saliency import find_top_k, find_min_count, find_salient

# When processing posts, ignore these words
STOP_WORDS = ['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                'but', 'by', 'course', 'for', 'from', 'how', 'i',
                'in', 'include', 'is', 'not', 'of', 'on', 'or', 's', 'so',
                'such', 'that', 'the', 'their', 'this', 'through', 'to',
                'we', 'were', 'which', 'will', 'with', 'yet', 'http']


def process_database(school_file):
    '''
    Given a csv database, process all text into a list of dictionaries
    Input: csv file
    Output: lst of post dictionaries (lst)
    '''
    post_lst = []
    with open(school) as csv_file:
        for row in csv.DictReader(csv_file, skipinitialspace = True):
            row_dict = {key : value for key, value in row.items()}
            post_lst.append(row_dict)
    return post_lst


def delete_stop_words():
    '''
    Given list of dictionaries, delete the STOP words listed at top of file
    Input: list of dict
    Output:
        list of 
    '''
