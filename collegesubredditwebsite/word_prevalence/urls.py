from django.urls import path

from . import views

urlpatterns = [
    path('word_prevalence.html', views.word_prevalence_view, name='wordprevalence'),
]