import requests
from django.shortcuts import render

def index(request, nb):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(nb)
    response = requests.get(url)
    pokemon = response.json()
    parsejson(pokemon)

    return render(request, 'pokedex/index.html', {'poke':pokemon})