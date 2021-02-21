"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
"""

from django.shortcuts import render
from django import forms
from nancy_find_suggested_posts import find_suggested_posts


class SearchForm(forms.Form):
    question = forms.CharField(
        label='Question',
        help_text=("""ex. what classes should I take"""),
        required=True)
    college = forms.CharField(
        label='College',
        help_text=("""ex. uchicago"""),
        required=False)

def find_suggested_posts_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            if form.cleaned_data["question"]:
                string_of_words = form.cleaned_data["question"]
            if form.cleaned_data["college"]:
                college = form.cleaned_data["college"]
            else:
                college = ""
            res = find_suggested_posts(string_of_words, college)
    
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        context['result'] = res

    return render(request, 'find_suggested_posts.html', context)