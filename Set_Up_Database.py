"""
References: https://www.programiz.com/python-programming/methods/built-in/filter
"""

import sqlite3
import pandas as pd
from nltk.corpus import stopwords

def create_words_csv():
    """
    This function retrieves the texts from the posts, as well
    as the unique post ids for each of the posts from the sql
    database, and it cleans the text. Ultimately, it creates a
    csv file of each word in the text with the unique post id
    and user id.
    """
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = "SELECT text, unique_post_id, user_id from post_info"
    r = c.execute(query)

    all_posts = r.fetchall()

    letters = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    df = pd.DataFrame()
    for post in all_posts:
        text, unique_post_id, user_id = post
        new_text = "".join(filter(letters.__contains__, text))
        new_text = new_text.lower()
        new_text = new_text.split()
        for new_word in new_text:
            if len(new_word) > 50:
                continue
            else:
                df = df.append({
                        "word": new_word,
                        "unique_post_id" : unique_post_id,
                        "user_id": user_id
                    }, ignore_index = True)
    df.to_csv("word_raw_data.csv", index = False, header = True)

def create_cleaned_text_and_titles():
    """
    This function retrieves the texts from the posts, as well
    as the unique post ids and titles for each of the posts from the sql
    database, and it cleans the text. Ultimately, it creates a
    csv file of the cleaned text with the unique post id and title.
    """
    db = sqlite3.connect("db.sqlite3")
    c = db.cursor()
    query = "SELECT text, unique_post_id from post_info"
    r = c.execute(query)

    all_posts = r.fetchall()
    letters = set("abcdefghijklmnopqrstuvwxyz ")
    df = pd.DataFrame()
    data = []
    for post in all_posts:
        text, unique_post_id = post
        text = text.lower()
        new_text = "".join(filter(letters.__contains__, text))
        new_text_tokens = new_text.split()
        filtered_text_tokens = [word for word in new_text_tokens if word not in stopwords.words("english")]
        filtered_text = ""
        for token in filtered_text_tokens:
            filtered_text += (token + " ")
        data.append([filtered_text, unique_post_id])
    
    df = pd.DataFrame(data, columns = ["text", "unique_post_id"])

    df.to_csv("filtered_text_data.csv", index = False, header = True)


        