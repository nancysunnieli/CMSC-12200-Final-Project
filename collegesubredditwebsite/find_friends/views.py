"""
References: 
https://www.youtube.com/watch?v=F5mRW0jo-U4
https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
PA3 from CMSC 12200
"""

from django.shortcuts import render
from django import forms
from nancy_find_friends import find_friends


class SearchForm(forms.Form):
    id = forms.CharField(
        label='Reddit Username',
        help_text=("""ex. turnip_master"""),
        required=True)

def find_friends_view(request):
    form = SearchForm()
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        context["form"] = form
        if form.is_valid():
            if form.cleaned_data["id"]:
                user_id = form.cleaned_data["id"]
                res = find_friends(user_id)
    
    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        context['result'] = res

    return render(request, 'find_friends.html', context)