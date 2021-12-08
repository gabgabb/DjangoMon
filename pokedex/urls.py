from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    #path('bellebite/', views.hello, name="bite"),
]