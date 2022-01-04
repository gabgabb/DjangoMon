from django.http.response import HttpResponseRedirect
import requests
import json
import logging
from django.shortcuts import render
from .forms import PokemonForm


def index(request, nb):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(nb)
    response = requests.get(url)
    pokemon = response.text
    parse_json = json.loads(pokemon)
    name = parse_json["names"][4]["name"]

    return render(request, 'pokedex/index.html', {'name':name})
    
def src_pokemon(request):    
    if request.method == 'POST':
        form = PokemonForm(request.POST)
        if form.is_valid():
            url = "https://pokeapi.co/api/v2/pokemon/" + str(form.data.get('pokemon'))
            response = requests.get(url)
            pokemon = response.text
            parse_json = json.loads(pokemon)
            id = parse_json["id"]
            logging.info(id)
            return HttpResponseRedirect(str(id))
    else:
        form = PokemonForm()
    


    