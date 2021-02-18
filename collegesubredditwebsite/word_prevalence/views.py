"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
"""

from django.shortcuts import render
from django import forms
from nancy_word_prevalence import create_graph

# Create your views here.

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

def graphic(res):

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

class SearchForm(forms.Form):
    start_date = forms.CharField(
        label='Start Date',
        help_text=("""In the form: MM/DD/YY.
         Earliest date for each college is as follows:
         caltech: 04/14/11,
          harvard: 09/13/19,
           jhu: 07/13/20,
            mit: 10/07/19,
             princeton: 04/01/15,
              stanford: 08/24/20,
               uchicago: 07/30/20,
                upenn: 10/05/20,
                 yale: 06/28/18,
                  columbia: 11/22/20"""),
        required=True)
    end_date = forms.CharField(
        label='End Date',
        help_text=("In the form: MM/DD/YY. Latest date is 02/16/21."),
        required=True)
    data_points = forms.IntegerField(
        label='Data Points',
        help_text='e.g. 5',
        required=True)
    college = forms.CharField(
        label='College',
        help_text=("""e.g. uchicago; If you want to do multiple colleges, 
        separate the name of the colleges by a space. Choices are as follows:
        uchicago, upenn, yale, caltech, mit, stanford, jhu,
        princeton, harvard, columbia"""),
        required=False)
    word = forms.CharField(
        label = 'Word',
        help_text = 'e.g. potato',
        required=True
    )

def word_prevalence_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            args = {}
            if form.cleaned_data['start_date'] and form.cleaned_data['end_date']:
                args['time frame'] = (form.cleaned_data['start_date'], form.cleaned_data['end_date'])
            data_points = form.cleaned_data['data_points']
            if data_points:
                args['data points'] = data_points
            college = form.cleaned_data['college']
            if college:
                args['college'] = []
                college = college.split()
                for college in college:
                    args['college'].append(college)
            word = form.cleaned_data['word']
            if word:
                args['word'] = word
            res = create_graph(args)
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        #context['result'] = res
        graphic1 = graphic(res)
        context["graphic"] = graphic1

    return render(request, 'word_prevalence.html', context)


