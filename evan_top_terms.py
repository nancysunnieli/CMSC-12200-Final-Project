'''
This task is to return the top k n-grams w/ the given parameters by the user being:
    1) the school name,
    2) the number of words you want to receive back (n-grams),
    3) the number of n-grams you want to see (k number of n-grams),

    4) the start and end time range you want to comb thru,
            (optional, assume all time otherwise)
    5) and the upote/downvote score (optional)
'''

import csv
import sys
import datetime
import unicodedata
from evan_word_saliency import find_top_k, find_salient
from nancy_word_prevalence import convert_date_time_to_epoch_time

# When processing posts, ignore these words
STOP_WORDS = ['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                'but', 'by', 'for', 'from', 'how', 'i',
                'in', 'include', 'is', 'not', 'of', 'on', 'or', 's', 'so',
                'such', 'that', 'the', 'their', 'this', 'through', 'to',
                'we', 'were', 'which', 'will', 'with', 'yet', 'if', 'does',
                'was']

# When processing posts, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp", "\n\n")

def process_database(school_name):
    '''
    Given a csv database, process all text into a list of dictionaries
    Input: school subreddit name
    Output: lst of post dictionaries (lst)
    '''
    post_lst = []
    with open('all_raw_data.csv') as csv_file:
        for row in csv.DictReader(csv_file, skipinitialspace = True):
            if row["subreddit"] == school_name:
                row_dict = {key : value for key, value in row.items()}
                post_lst.append(row_dict)
    return post_lst


def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&", "|"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])


def ignore_stop_words(redd_post):
    '''
    Given a dictionary, ignore the STOP words and STOP prefixes 
    listed at top of file from the posts to create an edited dict
    Input:
        redd_post: a dict
        stop (bool): whether to consider stop words or not
    Output:
        lst of strings (single post text edited to not
                        have stop words or prefixes)
    '''
    post_processed_text = []
    reddit_text = redd_post["text"]
    split_post = str.split(reddit_text)
    for i in split_post:
        word = i.strip(PUNCTUATION)
        if not word.startswith(STOP_PREFIXES):
            if word != '':
                lower_word = str.lower(word)
                if word not in STOP_WORDS and lower_word not in STOP_WORDS:
                    if word.find("|") == -1:
                        post_processed_text.append(word)
    return post_processed_text


def return_ngrams(redd_post, n, start_time, end_time, ratio_min, ratio_max):
    '''
    Creates a list of cleaned n-gram tuples from a single abridged post
    Inputs:
        redd_post (dict): a single Reddit post
        stop (bool): whether to consider stop words or not
        n (int): number of words in an n-grams
        start_time: MM/DD/YY (str)
        end_time: MM/DD/YY (str)
        ratio_min: int
        ratio_max: int
    Returns:
        n_grams_list (list): a list of n-grams as n-tuples
    '''
    if ratio_min <= float(redd_post["score"]) <= ratio_max:
        post_time = redd_post["epoch_time"]
        if (float(convert_date_time_to_epoch_time(start_time)) <= float(post_time)
                             and float(post_time) <= float(convert_date_time_to_epoch_time(end_time))):
            abridged_post = ignore_stop_words(redd_post)
            n_grams_list = []
            for i in range(0, len(abridged_post) - (n - 1)):
                n_gram = []
                for j in range(0, n):
                    n_gram.append(abridged_post[(i + j)])
                n_grams_list.append(tuple(n_gram))
            return n_grams_list
    return []


def all_ngrams(redd_posts, n, start_time, end_time, ratio_min, ratio_max):
    '''
    For a dictonary of Reddit posts, this function 
    creates a list of all its n-grams
    Inputs:
        school_file (csv): csv file
        stop (bool): whether to consider stop words or not
        n: the number of words in an n-gram
        start_time: MM/DD/YY (str)
        end_time: MM/DD/YY (str)
        ratio_min: int
        ratio_max: int
    Returns:
        all_ngrams_list: a list of all n-grams
    '''
    all_ngrams_list = []
    for post in redd_posts:
        all_ngrams_list.extend(return_ngrams(post, n, start_time, end_time,
                                            ratio_min, ratio_max))
    return all_ngrams_list


#this is the final function we call to get list of k-elements each comprising of n words
def find_top_k_ngrams(school_name, n, k, start_time='01/01/00', end_time='03/01/21', ratio_min=0, ratio_max=500):
    '''
    Find k most frequently occurring n-grams
    Inputs:
        school_file (csv): csv file
        n (int): the number of words in an n-gram
        k (int): a non-negative integer
        start_time: MM/DD/YY (str)
        end_time: MM/DD/YY (str)
        ratio_min: int
        ratio_max: int
    Returns: list of n-grams
    '''
    redd_posts = process_database(school_name)
    tuple_lst = find_top_k(all_ngrams(redd_posts, n, start_time,
                            end_time, ratio_min, ratio_max), k)
    final_lst = []
    for i in tuple_lst:
        final_str = ' '.join(i)
        final_lst.append(final_str)
    return final_lst


#do we even need saliency ?? 
def find_salient_ngrams(school_file, n, threshold):
    '''
    Find the salient n-grams for each tweet
    Inputs:
        school_file (csv): csv file
        n: integer parameter
        threshold (float): parameter
    Returns: list of sets of strings
    '''
    school_lst = process_database(school_file)
    list_of_list_ngrams = []
    for post in school_lst:
        list_of_list_ngrams.append(return_ngrams(post, n))
    return find_salient(list_of_list_ngrams, threshold)

