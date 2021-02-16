"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
"""

from django.shortcuts import render
from django import forms
from sarah_word_similarity import compute_percent_similar

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
    college1 = forms.CharField(
        label='First College',
        help_text=("""e.g. UChicago"""),
        required=True)
    college2 = forms.CharField(
        label = 'Second College',
        help_text = 'e.g. Caltech',
        required=True)
    ngram = forms.IntegerField(
        label = 'Amount of key words',
        help_text = 'e.g. 5',
        required=True
    )

def similarity_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start_date = form.cleaned_data['start_date']
            if form.cleaned_data['end_date']:
                 end_date = form.cleaned_data['end_date']
            if form.cleaned_data['college1']:
                college1 = form.cleaned_data['college1']
            if form.cleaned_data['college2']:
                college2 = form.cleaned_data['college2']
            if form.cleaned_data['ngram']:
                n = form.cleaned_data['ngram']
            res = compute_percent_similar(college1, college2,
                                          start_date, end_date, n)
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        context['result'] = res

    return render(request, 'similarity.html', context)


