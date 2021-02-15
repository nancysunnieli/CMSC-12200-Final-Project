
##################### THIS IS NOT EDITED MUCH #####################
##################### MY SALIENCY CODE FROM CS121 PA3 #####################

import math

def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens
    Inputs:
        tokens (list): list of tokens (must be immutable)
    Returns:
        token_count (dict): dictionary that maps tokens to counts
    '''
    token_count = {}
    for token in tokens:
        if token in token_count:
            token_count[token] = token_count[token] + 1
        else:
            token_count[token] = 1
    return token_count


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens
    Inputs:
        tokens (list): list of tokens (must be immutable)
        k (int): a non-negative integer
    Returns: list of the top k tokens ordered by count, larger first
    '''
    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")
    
    x = count_tokens(tokens)
    y = x.items()
    z = sort_count_pairs(y)
  
    count = k
    revised_list = []
    if k == 0:
        return revised_list
    for (i,j) in z:
        revised_list.append(i)
        count = count - 1
        if count == 0:
            break
    return revised_list


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times
    Inputs:
        tokens: a list of tokens (must be immutable)
        min_count: a non-negative integer
    Returns: set of tokens
    '''
    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")
    x = count_tokens(tokens)
    y = x.items()
    z = sort_count_pairs(y)
    count = min_count
    revised_list = []
    for (i,j) in z:
        if j >= count:
            revised_list.append(i)
    return set(revised_list)

def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.
    Inputs:
      docs (list): list of list of tokens
      threshold (float): parameter
    Returns: list of sets of salient words
    '''
    salient_list = []
    idf_score = find_idf_score(docs)
    for d in docs:
        tf_score = find_tf_score(d)
        salient_tokens = set()
        if len(tf_score) != None:
            for i in tf_score:
                j = tf_score.get(i,0)
                k = idf_score.get(i,0)
                tf_idf_score = j * k
                if tf_idf_score > threshold:
                    salient_tokens.add(i)
        salient_list.append(salient_tokens)
    return salient_list

def find_tf_score(d):
    '''
    Calculate the tf score for all unique terms in one doc
    Inputs:
        d (list): a document in docs
    Returns:
        x (dict): dictionary that maps token and tf value
    '''
    x = count_tokens(d)
    if len(x) > 0:
        max_freq = max(x.values())
        for key, value in x.items():
            tf_value = 0.5 + 0.5 * (value / max_freq)
            x[key] = tf_value
    return x


def find_idf_score(docs):
    '''
    Calculate idf score for each unique term in all docs

    Inputs:
        docs (list of lists): list of documents

    Returns:
        idf_score (dict): dictionary that maps unique token to idf score
    '''
    N = len(docs)
    idf_final_dict = {}
    unique_values_list = []
    for d in docs:
        x = count_tokens(d)
        for i in x:
            if i not in unique_values_list:
                unique_values_list.append(i)
    idf_score = []
    for i in unique_values_list:
        count = 0
        for d in docs:
            if i in d:
                count += 1
        idf_score.append(math.log( N / count))
    idf_final_dict = dict(zip(unique_values_list, idf_score))
    return idf_final_dict

def sort_count_pairs(l):
    '''
    Sort pairs using the second value as the primary sort key and the
    first value as the seconary sort key.

    Inputs:
       l: list of pairs.

    Returns: list of key/value pairs

    Example use:
    In [1]: import util

    In [2]: util.sort_count_pairs([('D', 5), ('C', 2), ('A', 3), ('B', 2)])
    Out[2]: [('D', 5), ('A', 3), ('B', 2), ('C', 2)]

    In [3]: util.sort_count_pairs([('C', 2), ('A', 3), ('B', 7), ('D', 5)])
    Out[3]: [('B', 7), ('D', 5), ('A', 3), ('C', 2)]
    '''
    return list(sorted(l, key=cmp_to_key(cmp_count_tuples)))
