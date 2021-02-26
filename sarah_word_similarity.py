# This task is to return the percent similarity in top word usage
# between two schools. The user specifies the schools, start and end
# dates, and the number of top terms to do the comparison on.

import nancy_word_prevalence as nwp
import evan_top_terms as ett
import matplotlib.pyplot as plt

SCHOOLS = ["caltech", "harvard", "jhu", "mit", "princeton", "stanford", "uchicago",
           "upenn", "yale", "columbia"]


def compute_percentages(words, school, start, end):
    '''
    Given a list of words and a school, compute percentage of content
    taken up by each word in the list and total percentage of content
    taken up by the list as a whole in the specified time range.

    Inputs: words (list of strings),
            school (string),
            start (epoch time),
            end (epoch time)

    Returns: total percentage of content taken up by words (float),
             dictionary mapping strings to percentages
    '''
    total_percentage = 0
    percentages = {}

    for word in words:
        perc = nwp.compute_word_as_percentage_of_all_words(start, end,
                                                           [school], word)
        total_percentage += perc
        percentages[word] = perc
    
    return total_percentage, percentages


def compute_percent_similar(school_1, school_2, start_date, end_date, k):
    '''
    Given two schools and two dates, computes the percentage overlap
    in the top n terms (1-grams) for that time period.

    Ex: If school 1 has terms "a" used 30% of the time and "b" used
    20% of the time for a total of 50% overall content, while school 2
    has terms "a" used 25% of the time and "b" used 50% of the time for
    a total of 75% overall content, we compute for school 1 that "a" and
    "b" constitute 60% and 40% of the top terms, and for school 2 that
    "a" and "b" constitute 33.3% and 66.7% of the top terms. We then take
    the minima and add: 33.3% + 40% = 73.3% similar for these 2 top terms.

    Inputs: two strings of college names,
            two strings of form "MM/DD/YY",
            k (integer)

    Returns: float
    '''
    top_k_1 = ett.find_top_k_ngrams(school_1, 1, k, start_date, end_date)
    top_k_2 = ett.find_top_k_ngrams(school_2, 1, k, start_date, end_date)
    overlap = []

    for word in top_k_1:
        if word in top_k_2:
            overlap.append(word)
    
    if not overlap:
        return 0

    start_epoch_date = nwp.convert_date_time_to_epoch_time(start_date)
    end_epoch_date = nwp.convert_date_time_to_epoch_time(end_date)
    
    total_percentage_1, top_percentages_1 = compute_percentages(overlap,
                                                        school_1,
                                                        start_epoch_date,
                                                        end_epoch_date)
    total_percentage_2, top_percentages_2 = compute_percentages(overlap,
                                                        school_2,
                                                        start_epoch_date,
                                                        end_epoch_date)
    
    percent_overlap = 0
    for word, perc_1 in top_percentages_1.items():
        relative_perc_1 = perc_1 / total_percentage_1
        relative_perc_2 = top_percentages_2[word] / total_percentage_2
        percent_overlap += min(relative_perc_1, relative_perc_2)
    
    return percent_overlap * 100


def compare_all(target_school, start_date, end_date, k):
    '''
    Generate a bar graph of percentage similarities between the target school
    and all other schools for a given time period and number of words.
    
    Referenced https://benalexkeen.com/bar-charts-in-matplotlib/
    
    Inputs: college name (string),
            two strings of form "MM/DD/YY",
            k (integer)
    
    Returns: figure
    '''
    x = []
    y = []
    for school in SCHOOLS:
        if school != target_school:
            x.append(school)
            y.append(compute_percent_similar(target_school, school, start_date,
                                             end_date, k))
    
    x_pos = [i for i, _ in enumerate(x)]

    fig = plt.figure()
    plt.bar(x_pos, y)
    plt.xticks(x_pos, x, rotation='vertical')
    plt.title("Top " + str(k) + " word(s) usage similarities vs " + target_school)
    plt.xlabel("school")
    plt.ylabel("percent similar")
    
    
    # Comment this in if you want to run this program from
    # ipython3 instead of the website
    # plt.show()
    
    return fig
