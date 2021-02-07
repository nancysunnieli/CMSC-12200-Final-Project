CREATE TABLE post_info
    (downs integer,
    epoch_time integer,
    score floats(5, 3),
    subreddit varchar(50),
    text varchar(8000),
    title varchar(100),
    unique_post_id varchar(20),
    ups integer,
    upvote_ratio float(5, 3));

.separator ","

.import all_raw_data.csv post_info

CREATE TABLE post_words
    (unique_post_id varchar(20),
    word varchar(200));

.separator ","

.import words_raw_data.csv post_words
