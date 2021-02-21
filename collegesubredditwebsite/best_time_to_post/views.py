"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
"""

from django.shortcuts import render
from django import forms
from jingwen_scores_trend import main

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
    college = forms.CharField(
        label='College',
        help_text=("""e.g. UChicago"""),
        required=True)

def best_time_to_post_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            college = form.cleaned_data['college']
            res = main({"college": college})
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        graphic1 = graphic(res)
        context["graphic"] = graphic1

    return render(request, 'best_time_to_post.html', context)