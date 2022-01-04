from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:nb>', views.index, name="index"),
    path('src_pokemon', views.src_pokemon, name="src_pokemon"),
    #path('bellebite/', views.hello, name="bite"),
]