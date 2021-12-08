import requests
import json
from django.shortcuts import render

def index(request, nb):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(nb)
    response = requests.get(url)
    pokemon = response.text
    parse_json = json.loads(pokemon)
    name = parse_json["names"][4]["name"]

    return render(request, 'pokedex/index.html', {'name':name})