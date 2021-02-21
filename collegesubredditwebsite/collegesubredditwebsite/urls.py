"""collegesubredditwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from pages.views import (home_view, about_view)
from word_prevalence.views import word_prevalence_view
from similarity.views import similarity_view
from top_keywords.views import top_keywords_view
from best_time_to_post.views import best_time_to_post_view
from find_friends.views import find_friends_view
from find_suggested_posts.views import find_suggested_posts_view

urlpatterns = [
    path('', home_view, name = 'home1'),
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('word_prevalence/', word_prevalence_view, name='word_prevalence'),
    path('similarity/', similarity_view, name='similarity'),
    path('top_keywords/', top_keywords_view, name='top_keywords'),
    path('best_time_to_post/', best_time_to_post_view, name='best_time_to_post'),
    path('find_friends/', find_friends_view, name='find_friends'),
    path('find_suggested_posts/', find_suggested_posts_view, name='find_suggested_posts'),
]
