"""
Data sources:
reddit APIs

References: https://alpscode.com/blog/how-to-use-reddit-api/
            https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
"""
 # Requesting a temporary OAuth token from Reddit

import requests
import pandas as pd

base_url = "https://www.reddit.com/"
data = {"grant_type": "password", "username": "cmsc12200", "password": "cmsc122002021"}
auth = requests.auth.HTTPBasicAuth("NcnHg9YC03jQNg", "Ayx-RuhcCgs6ii_30ElHE9O1Bu-cCw")
headers = {"User-agent": "keyword-search by cmsc12200"}
r = requests.post(base_url + "api/v1/access_token",
                    data = data,
                    headers = headers,
                    auth = auth)

TOKEN = r.json()["access_token"]

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


# Scraping Colleges
# Colleges to Scrape:
# Harvard, Princeton, Columbia, MIT, Yale, Stanford, UChicago, UPenn, Caltech, JHU


list_of_schools = ["Harvard", "Princeton", "Yale", "MIT", "Columbia",
                     "Stanford", "UChicago", "UPenn", "Caltech", "JHU"]




df = pd.DataFrame()

#pulling title, date-time, content, and reactions to a post

for school in list_of_schools:
    last_post = None
    for i in range(20):
        r = requests.get("https://oauth.reddit.com/r/" + school + "/new",
                          headers=headers,
                          params= {"limit": "100", "after": last_post})
        for post in r.json()["data"]["children"]:
            df = df.append({
                "subreddit": (post["data"]["subreddit"]).lower(),
                "title" : post["data"]["title"],
                "text": post["data"]["selftext"],
                "upvote_ratio": post["data"]["upvote_ratio"],
                "ups":post["data"]["ups"],
                "downs": post["data"]["downs"],
                "score": post["data"]["score"],
                "epoch_time": post["data"]["created_utc"],
                "unique_post_id": post["data"]["name"],
                "user_id": post["data"]["author"]
            }, ignore_index = True)
        last_post = post["data"]["name"]
    
    # This creates a separate csv for every school
    # To create "all_raw_data.csv", delete the following two lines
    # and add the following line of code outside of the for loop:
    # df.to_csv("all_raw_data.csv", index = False, header = True)
    df.to_csv(school + "_raw_data.csv", index = False, header = True)
    df = pd.DataFrame()


