# -*- encoding: utf-8 -*-
"""

"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    path('', views.overview, name='home'),
    path('home/', views.overview, name='home'),
    path('results/<survey_id>', views.results, name='results'),

    path('all_user_responses/', views.all_user_responses, name='all_user_responses'), 
    path('users/', views.users, name='users'),
    path('surveys/', views.surveys, name='surveys'),

    path('all_groups/', views.all_groups, name='all_groups'),

    path('new_user/', views.new_user, name='new_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('user_details/', views.user_details, name='user_details'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('all_users/', views.all_users, name='all_users'),

    path('all_questions/', views.all_questions, name='all_questions'),
    path('new_survey/', views.new_survey, name='new_survey'),
    path('edit_survey/', views.edit_survey, name='edit_survey'),
    path('survey_details/', views.survey_details, name='survey_details'),
    path('delete_survey/', views.delete_survey, name='delete_survey'),
    path('finish_survey/', views.finish_survey, name='finish_survey'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
