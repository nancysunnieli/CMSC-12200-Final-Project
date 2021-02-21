CREATE TABLE post_info
    (downs integer,
    epoch_time integer,
    score floats(5, 3),
    subreddit varchar(50),
    text varchar(8000),
    title varchar(100),
    unique_post_id varchar(20),
    ups integer,
    upvote_ratio float(5, 3),
    user_id varchar(100));

.separator ","

.import all_raw_data.csv post_info

CREATE TABLE post_words
    (unique_post_id varchar(20),
    user_id varchar(100),
    word varchar(200));

.separator ","

.import word_raw_data.csv post_words

CREATE TABLE filtered_text
    (text varchar(8000),
    unique_post_id varchar(20));

.separator ","

.import filtered_text_data.csv filtered_text
