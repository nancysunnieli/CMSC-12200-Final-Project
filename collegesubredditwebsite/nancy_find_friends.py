"""
https://medium.com/@sumn2u/cosine-similarity-between-two-sentences-8f6630b0ebb7
https://stackoverflow.com/questions/28819272/python-how-to-calculate-the-cosine-similarity-of-two-word-lists

"""

import sqlite3
from nltk.corpus import stopwords
from math import sqrt
from collections import Counter

def create_list_of_other_users(user_id):
    """
    This returns back a list of the other users in the database.

    Inputs:
    user_id (string): name of original user

    Outputs:
    all_other_users (list of strings): list of names of other users
    """
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = ("SELECT user_id FROM post_info")
    r = c.execute(query)
    all_other_users = r.fetchall()
    all_other_users = list(set(all_other_users))
    all_users_edited = []
    for user in all_other_users:
        user = str(user).strip("(),'")
        all_users_edited.append(user)
    
    all_users_edited.remove(user_id)
    all_users_edited.remove('[deleted]')
    return all_users_edited

def create_list_of_words(user_id):
    """
    Creates a list of all the words that a given user uses.
    Then cleans this list to get rid of words that don't add meaning.

    Inputs:
    user_id (string): name of original user

    Outputs:
    all_words (list of strings): list of all the words that the user has used
    """
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = ("SELECT text FROM post_info WHERE user_id = ?")
    params = [user_id]
    r = c.execute(query, params)
    all_posts = r.fetchall()
    all_posts_edited = []

    letters = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for post in all_posts:
        new_post = str(post).strip("(,)")
        new_post = "".join(filter(letters.__contains__, new_post))
        all_posts_edited.append(new_post)
    return all_posts_edited

def compute_cosine_similarity(first_user_list, second_user_list):
    """
    Computes the cosine similarity between two lists of words.

    Inputs:
    first_user_list (list of strings): The first list of words
    second_user_list (list of strings): The second list of words

    Outputs:
    cosine_similarity (float): The cosine similarity between the two lists
    """

    all_words_first_list = []
    for post in first_user_list:
        new_post = post.split()
        all_words_first_list += new_post
    
    all_words_second_list = []
    for post in second_user_list:
        new_post = post.split()
        all_words_second_list += new_post

    all_words = set(all_words_first_list + all_words_second_list)
    counted_first_user = Counter(all_words_first_list)
    counted_second_user = Counter(all_words_second_list)

    first_vector = [counted_first_user.get(word, 0) for word in all_words]
    second_vector = [counted_second_user.get(word, 0) for word in all_words]

    len_first = sqrt(sum(num ** 2 for num in first_vector))
    len_second = sqrt(sum(num ** 2 for num in second_vector))

    dot_product = sum(num1 * num2 for num1, num2 in zip(first_vector, second_vector))

    if len_first != 0 and len_second != 0:
        cosine = (dot_product/(len_first * len_second)) * 100
    else:
        cosine = 0
    return cosine

def find_friends(user_id):
    """
    Given a user_id, this function returns back a list of all the other users
    in the order of which ones are the most similar to them based on the topics and words
    that they use in their posts.

    Inputs:
    user_id (string): name of the user

    Outputs:
    top_hundred (list of tuples): 100 most similar users with a sample post
    """
    original_user_words = create_list_of_words(user_id)
    all_other_users = create_list_of_other_users(user_id)
    
    all_other_users_words = {}

    for other_user in all_other_users:
        other_user_words = create_list_of_words(other_user)
        if other_user_words != [""]:
            all_other_users_words[other_user] = other_user_words
    
    cosine_similarity = {}
    for other_user, other_user_words in all_other_users_words.items():
        similarity_measure = compute_cosine_similarity(original_user_words, other_user_words)
        cosine_similarity[tuple((other_user, other_user_words[0][0:100]))] = similarity_measure
    
    sorted_cosine_similarity = sorted(cosine_similarity, key = cosine_similarity.get, reverse = True)
    top_hundred = sorted_cosine_similarity[:100]

    return top_hundred