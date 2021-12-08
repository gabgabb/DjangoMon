import requests
from django.shortcuts import render

def index(request):
    url = "https://pokeapi.co/api/v2/pokemon?limit=10&offset=0"
    response = requests.get(url)
    pokemon = response.json()

    return render(request, 'pokedex/index.html', {'poke':pokemon})