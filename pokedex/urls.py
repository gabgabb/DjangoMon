from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:nb>', views.index, name="index"),
    path('acceuil/', views.pageAcceuil),
    path('acceuil/<int:offset>/<int:limit>', views.pageAcceuil, name="acceuil"),
    path('src_pokemon', views.src_pokemon, name="src_pokemon"),
    path('acceuil/src_pokemon', views.src_pokemon, name="src_pokemon"),
]