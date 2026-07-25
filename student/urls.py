from django.shortcuts import render, redirect
from django.urls import path
from student import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]