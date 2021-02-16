"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
https://stackoverflow.com/questions/56714856/how-can-i-show-wordcloud-in-html
"""

from django.shortcuts import render
from django import forms
from evan_top_terms import find_top_k_ngrams, create_word_cloud

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import urllib

def graphic(res):
    plt.imshow(res, interpolation = 'bilinear')
    plt.axis("off")
    image = BytesIO()
    plt.savefig(image, format = 'png')
    image.seek(0)
    string = base64.b64encode(image.read())
    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64

# Create your views here.

class SearchForm(forms.Form):
    start_date = forms.CharField(
        label='Start Date',
        help_text=("""In the form: MM/DD/YY.
         Earliest date for each college is as follows:
         Caltech: 04/14/11,
          Harvard: 09/13/19,
           JHU: 07/13/20,
            MIT: 10/07/19,
             Princeton: 04/01/15,
              Stanford: 08/24/20,
               UChicago: 07/30/20,
                UPenn: 10/05/20,
                 Yale: 06/28/18"""),
        required=True)
    end_date = forms.CharField(
        label='End Date',
        help_text=("In the form: MM/DD/YY"),
        required=True)
    number_of_words_n_gram = forms.IntegerField(
        label='Number of Words in N-Gram',
        help_text='e.g. 2',
        required=True)
    college = forms.CharField(
        label='College',
        help_text=("""e.g. UChicago; If you want to do all colleges, type in All"""),
        required=True)
    number_of_key_words = forms.IntegerField(
        label = 'Number of Key Words',
        help_text = 'e.g. 5',
        required=True)
    minimum_ratio = forms.FloatField(
        label = 'Minimum Ratio',
        help_text = 'e.g. 0.1',
        required=True
    )
    maximum_ratio = forms.FloatField(
        label = 'Maximum Ratio',
        help_text = 'e.g. 0.5',
        required=True
    )

def top_keywords_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            start_time = form.cleaned_data['start_date']
            end_time = form.cleaned_data['end_date']
            n = form.cleaned_data['number_of_words_n_gram']
            k = form.cleaned_data['number_of_key_words']
            school_file = form.cleaned_data['college'] + "_raw_data.csv"
            ratio_min = form.cleaned_data['minimum_ratio']
            ratio_max = form.cleaned_data['maximum_ratio']

            res = find_top_k_ngrams(school_file, n, k, start_time, end_time, ratio_min, ratio_max)
            wordcloud = create_word_cloud(school_file, n, k, start_time, end_time, ratio_min, ratio_max)
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        context['result'] = res
        context["graphic"] = graphic(wordcloud)

    return render(request, 'top_keywords.html', context)