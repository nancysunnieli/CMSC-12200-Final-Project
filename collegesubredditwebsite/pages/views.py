from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def word_prevalence_view(request, *args, **kwargs):
    return render(request, "word_prevalence.html", {})

def top_keywords_view(request, *args, **kwargs):
    return render(request, "top_keywords.html", {})

def similarity_view(request, *args, **kwargs):
    return render(request, "similarity.html", {})

def up_votes_view(request, *args, **kwargs):
    return render(request, "up_votes.html", {})

def submit(request):
    info = request.POST['info']