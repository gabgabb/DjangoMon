import random
import time
import requests
import json
import aiohttp
import asyncio
import logging

from django.shortcuts import render, redirect
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


async def pageAccueil(request, offset=0, limit=30):
    start_time = time.time()  # timer

    urlAllPokemon = "https://pokeapi.co/api/v2/pokemon/?offset=" + str(offset) + "&limit=" + str(limit)
    responseAllPokemon = requests.get(urlAllPokemon).text
    parse_AllPokemon = json.loads(responseAllPokemon)

    urlSpecies = "https://pokeapi.co/api/v2/pokemon-species/?offset=" + str(offset) + "&limit=" + str(limit)
    species1 = requests.get(urlSpecies).text
    species2 = json.loads(species1)

    actionsAllPokemon = []
    actionsAllSpecies = []
    dataRender = []

    if limit >= 30 or offset < limit:
        async with aiohttp.ClientSession() as session:
            for i in range(limit - offset):
                url_ALl = parse_AllPokemon["results"][i]["url"]
                url_all_species = species2["results"][i]["url"]

                actionsAllPokemon.append(asyncio.ensure_future(getPokemonData(session, url_ALl)))
                actionsAllSpecies.append(asyncio.ensure_future(getPokemonData(session, url_all_species)))

            print("--- %s seconds gather0 ---" % (time.time() - start_time))
            result = await asyncio.gather(*actionsAllPokemon)
            print("--- %s seconds gather1 ---" % (time.time() - start_time))
            result2 = await asyncio.gather(*actionsAllSpecies)
            print("--- %s seconds gather2 ---" % (time.time() - start_time))


            for i, pokemonList in enumerate(result):
                pokemonJson = json.loads(json.dumps(pokemonList))
                nameFrench = json.loads(json.dumps(result2[i]))["names"][4]["name"]
                # pokemonSpeciesList = await asyncio.gather(getPokemonData(session, pokemonJson["species"]["url"]))
                # nameFrench = json.loads(requests.get(pokemonJson["species"]["url"]).text)["names"][4]["name"]
                spriteUrl = pokemonJson["sprites"]["other"]["official-artwork"]["front_default"]
                dataRender.append({"id": i + offset + 1, "name": nameFrench, "sprite": spriteUrl})

        print("--- %s seconds END ---" % (time.time() - start_time))
        return render(request, 'pokedex/accueil.html', {'data': dataRender, 'offset': offset, 'limit': limit})
    else:
        return redirect('accueil')


async def getPokemonData(session, url):
    async with session.get(url) as result:
        dataPokemon = await result.json()
        return dataPokemon


def src_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST)
        if form.is_valid():
            url = "https://pokeapi.co/api/v2/pokemon/" + str(form.data.get('pokemon'))
            response = requests.get(url)
            pokemon = response.text
            parse_json = json.loads(pokemon)
            id = parse_json["id"]
            return redirect('index', str(id))
        else:
            return redirect('index', str(random.randint(1, 1117)))

