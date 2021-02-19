"""
References: https://www.programiz.com/python-programming/methods/built-in/filter
"""

import sqlite3
import pandas as pd

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
