
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


def cmp_to_key(mycmp):
    '''
    Convert a cmp= function into a key= function
    From: https://docs.python.org/3/howto/sorting.html
    '''

    class CmpFn:
        '''
        Compare function class.
        '''
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return CmpFn


def cmp_count_tuples(t0, t1):
    '''
    Compare pairs using the second value as the primary key and the
    first value as the secondary key.  Order the primary key in
    non-increasing order and the secondary key in non-decreasing
    order.
    Inputs:
        t0: pair
        t1: pair
    Returns: -1, 0, 1
    Sample uses:
        cmp(("A", 3), ("B", 2)) => -1
        cmp(("A", 2), ("B", 3)) => 1
        cmp(("A", 3), ("B", 3)) => -1
        cmp(("A", 3), ("A", 3))
    '''
    (key0, val0) = t0
    (key1, val1) = t1
    if val0 > val1:
        return -1

    if val0 < val1:
        return 1

    if key0 < key1:
        return -1

    if key0 > key1:
        return 1

    return 0
