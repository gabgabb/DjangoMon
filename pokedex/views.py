from django.http.response import HttpResponseRedirect
import requests
import json
import logging
from django.shortcuts import render
from .forms import PokemonForm

def index(request, nb):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(nb)
    urlPokemon = "https://pokeapi.co/api/v2/pokemon/" + str(nb)

    responsePokemon = requests.get(urlPokemon)
    poke = responsePokemon.text
    parse_pokemon = json.loads(poke)
    spriteUrl = parse_pokemon["sprites"]["other"]["official-artwork"]["front_default"]

    response = requests.get(url)
    pokemon = response.text
    parse_json = json.loads(pokemon)
    name = parse_json["names"][4]["name"]

    return render(request, 'pokedex/index.html', {'name': name, 'sprite': spriteUrl})


def pageAcceuil(request, offset=0, limit=30):
    urlAllPokemon = "https://pokeapi.co/api/v2/pokemon/?offset=" + str(offset) + "&limit=" + str(limit)
    responseAllPokemon = requests.get(urlAllPokemon).text
    parse_AllPokemon = json.loads(responseAllPokemon)
    data = []

    for i in range(limit - offset):
        url_ALl = parse_AllPokemon["results"][i]["url"]

        responsePokemon = requests.get(url_ALl).text
        parse_Pokemon = json.loads(responsePokemon)
        name = parse_AllPokemon["results"][i]["name"]
        spriteUrl = parse_Pokemon["sprites"]["other"]["official-artwork"]["front_default"]

        data.append({"id": i + offset + 1, "name": name, "sprite": spriteUrl})

    return render(request, 'pokedex/acceuil.html', {'data': data, 'offset': offset, 'limit': limit})


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
