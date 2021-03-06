from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:nb>', views.index, name="index"),
    path('accueil/', views.pageAccueil, name="accueil"),
    path('accueil/<int:offset>/<int:limit>', views.pageAccueil, name="accueil"),
    path('src_pokemon', views.src_pokemon, name="src_pokemon"),
    path('accueil/src_pokemon', views.src_pokemon, name="src_pokemon"),
    path('team/', views.team_pokemon, name="team_pokemon"),
    path('team/<int:nb>', views.addPokemon, name="add_pokemon"),
    path('teamDel/<int:nb>', views.delPokemon, name="del_pokemon")
]