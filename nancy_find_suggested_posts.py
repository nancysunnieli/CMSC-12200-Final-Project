"""
Given an input of a string of words, as well as a college (optional),
it will return back a list of suggested posts
"""
import sqlite3
from nancy_find_friends import compute_cosine_similarity

def create_list_of_posts(college=""):
    """
    Goes through the database to create a list of relevant posts.

    Inputs: 
    college (string): name of college

    Outputs:
    cleaned_relevant_posts (list of tuples): list of tuples containing
    information of title, text, and unique_post_id
    """
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = ("""SELECT filtered_text.unique_post_id, filtered_text.text,  
                post_info.title FROM filtered_text JOIN post_info 
                ON filtered_text.unique_post_id = post_info.unique_post_id""")
    
    if college != "":
        query += " WHERE post_info.subreddit = ?"
        params = [college]
        r = c.execute(query, params)
    else:
        r = c.execute(query)
    all_relevant_posts = r.fetchall()
    
    return all_relevant_posts


def find_suggested_posts(string_of_words, college = ""):
    """
    Given a string of words and a college name from the user, it returns back
    posts that might be relevant.

    Inputs:
    string_of_words (string): a string of words
    college (string): name of a college

    Outputs:
    top_twenty (list of tuples): tuple of unique_post_id and title of post.
    It is the top twenty most similar posts.
    """
    cleaned_relevant_posts = create_list_of_posts(college)

    cosine_similarity = {}
    for unique_post_id, text, title in cleaned_relevant_posts:
        similarity_measure = compute_cosine_similarity(string_of_words.lower(), (title + text).lower())
        cosine_similarity[(unique_post_id, title)] = similarity_measure
    
    sorted_cosine_similarity = sorted(cosine_similarity, key = cosine_similarity.get, reverse = True)
    top_twenty = sorted_cosine_similarity[:20]

    return top_twenty
