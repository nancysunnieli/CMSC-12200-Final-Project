'''
This task is to return the top k n-grams w/ the given parameters by the user being:
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
                'we', 'were', 'which', 'will', 'with', 'yet']

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp", "\n\n")

def process_database(school_file):
    '''
    Given a csv database, process all text into a list of dictionaries
    Input: csv file
    Output: lst of post dictionaries (lst)
    '''
    post_lst = []
    with open(school_file) as csv_file:
        for row in csv.DictReader(csv_file, skipinitialspace = True):
            row_dict = {key : value for key, value in row.items()}
            post_lst.append(row_dict)
    return post_lst


def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])


def ignore_stop_words(redd_posts, stop):
    '''
    Given list of dictionaries, ignore the STOP words and STOP prefixes 
    listed at top of file from the posts to create an edited ver
    Input:
        redd_posts (lst): list of dict
        stop (bool): whether to consider stop words or not
    Output:
        list of edited dict items
    '''
    post_processed_text = []
    redd_post = redd_posts["text"]
    split_post = str.split(redd_post)
    for i in split_post:
        word = i.strip(PUNCTUATION)
        if word.startswith(STOP_PREFIXES) == False:
            if word != '':
                if stop == True:
                    if word not in STOP_WORDS:
                        post_processed_text.append(word)
                else:
                    post_processed_text.append(word)
    return post_processed_text


def return_ngrams(tweet, stop, case_sensitive, n):
    '''
    Creates a list of cleaned n-gram tuples from a single abridged text tweet
    Inputs:
        tweet (dict): a single tweet
        stop (bool): whether to consider stop words or not
        case_sensitive (bool): whether word is case-sensitive or not
        n (int): number of words in an n-grams
    Returns:
        n_grams_list (list): a list of n-grams as n-tuples
    '''
    abridged_tweet = do_pre_processing(tweet, 
                                stop, case_sensitive)
    n_grams_list = []
    for i in range(0, len(abridged_tweet) - (n - 1)):
        n_gram = []
        for j in range(0, n):
            n_gram.append(abridged_tweet[(i + j)])
        n_grams_list.append(tuple(n_gram))
    return n_grams_list


def all_ngrams(redd_posts, stop, n):
    '''
    For a dictonary of Reddit posts, this function 
    creates a list of all its n-grams
    Inputs:
        redd_posts (list): a list of dicts
        stop (bool): whether to consider stop words or not
        n: the number of words in an n-gram
    Returns:
        all_ngrams_list: a list of all n-grams
    '''


def find_top_k_ngrams(tweets, n, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets (list): a list of tweets
        n (int): the number of words in an n-gram
        case_sensitive (bool): a boolean that is True
                        if the task is case sensitive
        k (int): a non-negative integer

    Returns: list of n-grams
    '''
    return find_top_k(all_ngrams(tweets, 
                        True, n), k)


def find_salient_ngrams(tweets, n, threshold):
    '''
    Find the salient n-grams for each tweet
    Inputs:
        tweets (list): a list of tweets
        n: integer parameter
        case_sensitive: boolean
        threshold (float): parameter
    Returns: list of sets of strings
    '''
    list_of_list_ngrams = []
    for tweet in tweets:
        list_of_list_ngrams.append(return_ngrams(tweet, 
                                False, case_sensitive, n))
    return find_salient(list_of_list_ngrams, threshold)