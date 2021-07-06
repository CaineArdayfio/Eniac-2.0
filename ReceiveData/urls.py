# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from ReceiveData import views

urlpatterns = [
    path('receive/', views.receive, name='receive'),
    path('get_data/', views.get_data, name='get_data')
]
