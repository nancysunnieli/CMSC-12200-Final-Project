Name of Group: JSEN

Group Members: Sarah Zhang, Evan Xiang, Jingwen Zhang, Nancy Li
Description of Project: Scraping college subreddits on Reddit and creating lists of
most popular keywords from different colleges. Users enter the college, time
frame, and task they want accomplished. The scope of the project will be limited to
the ten top colleges according to USNews.

Goals of Project:
- The goal is to be able to scrape college subreddits
- It will return most popular keywords/phrases from the subreddits for a given
time period
- This will give us an idea of the interests of the student body at a
particular college during a particular time period.
- It will also compare percentage similarities across colleges
- This same functionality can also compare percentage similarities of
the same college across time periods
- It will also analyze word prevalence over time
- It can create a graph that will show the word prevalence as a
percentage of total words over time
- It will also analyze upvotes

Data Sources We Plan to Use :
HTML and API from subreddit links

Helpful Resources:
https://nycdatascience.com/blog/student-works/web-scraping-reddit-analyzing
-user-behavior-and-top-content-from-a-marketing-perspective/?fbclid=IwAR
0_Tj_xhSY6nXfLOMoTeewchjOmp-Y_sCWC_i4fq-aq8NRg5kdR2ZjQL9c
https://www.datacamp.com/community/tutorials/wordcloud-python?fbclid=I
wAR2uJhVRDPQ1aH0FeS_9FiZfDsGL7VlTQd_FVeKba064QCI8DTQwTu7
RvEU

Lists of Tasks to Complete and Timeline for Completing them:
Each of us is responsible for one of the above tasks.
Nancy: Analyzing word prevalence over time
Evan/Sarah: Percentage Similarities/ Top Keywords
Jingwen: Analyzing upvotes

Week 4
- Presentation

Week 5
- Collect data (all ten schools)
- Research characteristics of database that we will need to accomplish each of
our tasks
- Have meeting about this, and discuss how best to proceed in creating
database (what characteristics will the tables have? How will we be
representing the data?)
- Begin building database

Week 6
- Create algorithm to clean data (for one school)
- Create corpus of insignificant/repetitive words (from one school, limited
data)
- Set up database for one school
- Get database working for one school, so that the method can be applied to
the rest of the data
- Clean remaining data and add to database
- THE DATABASE SHOULD BE FINISHED AT THE END OF WEEK 6

Week 7-8
- Each team member works on their designated task separately
- Then, we will integrate all the programs so that it runs cohesively


DATA INFO:

Caltech:  April 14, 2011
Harvard: September 13, 2019
JHU: July 13, 2020 
MIT: October 7, 2019 
Princeton: April 1, 2015
Stanford: August 24, 2020
UChicago: July 30, 2020
UPenn: December 5, 2020
Yale: June 28, 2018





To run the program:
1.) Enter the directory called "collegesubredditwebsite". To do this, run the following command in your terminal: "cd collegesubredditwebsite".
2.) Enter the follwing command in the terminal: "python3 manage.py runserver".
2.) This will output a link. Copy and paste the link in the desired internet browser.
3.) Explore the pages on the website, which are as follows:
  - Home: This is a welcome message
  - About: This gives an explanation of the project and the pages
  - Top Keywords: This outputs the top keywords given parameters from the user
  - Word Prevalence: This outputs a graph of the percentage usage of a given word over time given parameters from the user
  - Similarity: The compares the similarity of two colleges given parameters from the user
  - Upvotes Analysis: This provides an analysis of the upvotes on the posts given parameters from the user
  
 
Description of files in this repository: <br />
1.) csv files:  <br />
  1.) word_raw_data.csv maps words to the post they are from. <br />
  2.) all_raw_data.csv contains all the raw data that was scraped from reddit APIs. It has the following columns: downs (number of down votes), epoch_time (time of post in epoch time), score (computed by reddit), subreddit (name of college the post is from), text (the raw text of the post), title (the title of the post), unique_post_id (unique post id), ups (amount of up votes), upvote_ratio (ratio between up and down votes). <br />
  3.) Yale_raw_data.csv, Stanford_raw_data.csv, UPenn_raw_data.csv, UChicago_raw_data.csv, Princeton_raw_data.csv, MIT_raw_data.csv, JHU_raw_data.csv, Harvard_raw_data.csv, and Caltech_raw_data.csv contain the same data as all_raw_data.csv. The difference is that it splits the data up by college.  <br /><br />
  
2.) reddit_scraping.py: this was the program used to scrape reddit APIs. <br /><br />
3.) Set_Up_Database.py and create_tables_in_sql: these were used to set up the db.sqlite3 database using the csv files. <br /><br />


4.) nancy_word_prevalence.py: this was the program used to create the word prevalence graphs  <br /><br />

5.) collegesubredditwebsite directory: This contains all the necessary files for the website.  
