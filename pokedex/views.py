import random
import requests
import json
import aiohttp
import asyncio
import logging
import string

from django.shortcuts import render, redirect
from .forms import PokemonForm


def index(request, nb):
    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(nb)
    urlPokemon = "https://pokeapi.co/api/v2/pokemon/" + str(nb)

    responsePokemon = requests.get(urlPokemon).text
    parse_pokemon = json.loads(responsePokemon)
    spriteUrl = parse_pokemon["sprites"]["other"]["official-artwork"]["front_default"]

    response = requests.get(url).text
    parse_json = json.loads(response)
    name = parse_json["names"][4]["name"]
    poids = parse_pokemon["weight"] / 10
    taille = parse_pokemon["height"] / 10

    habitatUrl = parse_json["habitat"]["url"]
    responseHabitat = requests.get(habitatUrl)
    parse_habitat = json.loads(responseHabitat.text)
    habitatFrench = parse_habitat["names"][0]["name"]

    typesAPI = parse_pokemon["types"]
    types = []
    colors = []

    for i in range(len(typesAPI)):
        urlType = parse_pokemon["types"][i]["type"]["url"]
        responseType = requests.get(urlType).text
        parse_type = json.loads(responseType)
        typeFrench = parse_type["names"][3]["name"]
        types.append(typeFrench)
        colors.append(colorType(typeFrench))

    return render(request, 'pokedex/index.html',
                  {'name': name, 'sprite': spriteUrl, 'poids': poids, 'taille': taille, 'habitat': habitatFrench,
                   'types': types, 'color': colors})


async def pageAccueil(request, offset=0, limit=32):
    urlAllPokemon = "https://pokeapi.co/api/v2/pokemon/?offset=" + str(offset) + "&limit=" + str(limit)
    responseAllPokemon = requests.get(urlAllPokemon).text
    parse_AllPokemon = json.loads(responseAllPokemon)

    urlSpecies = "https://pokeapi.co/api/v2/pokemon-species/?offset=" + str(offset) + "&limit=" + str(limit)
    species1 = requests.get(urlSpecies).text
    species2 = json.loads(species1)

    actionsAllPokemon = []
    actionsAllSpecies = []
    dataRender = []

    if limit >= 32 or offset < limit:
        async with aiohttp.ClientSession() as session:
            for i in range(limit - offset):
                url_ALl = parse_AllPokemon["results"][i]["url"]
                url_all_species = species2["results"][i]["url"]

                actionsAllPokemon.append(asyncio.ensure_future(getPokemonData(session, url_ALl)))
                actionsAllSpecies.append(asyncio.ensure_future(getPokemonData(session, url_all_species)))

            result = await asyncio.gather(*actionsAllPokemon)
            result2 = await asyncio.gather(*actionsAllSpecies)
            await session.close()

            for i, pokemonList in enumerate(result):
                pokemonJson = json.loads(json.dumps(pokemonList))
                nameFrench = json.loads(json.dumps(result2[i]))["names"][4]["name"]
                spriteUrl = pokemonJson["sprites"]["other"]["official-artwork"]["front_default"]
                dataRender.append({"id": i + offset + 1, "name": nameFrench, "sprite": spriteUrl})

        return render(request, 'pokedex/accueil.html', {'data': dataRender, 'offset': offset, 'limit': limit})
    else:
        return redirect('accueil')


async def getPokemonData(session, url):
    async with session.get(url) as result:
        dataPokemon = await result.json()
        return dataPokemon


async def src_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST)
        if form.is_valid():
            actionsAllPokemon = []
            async with aiohttp.ClientSession() as session:
                for i in range(1,890):
                    url = "https://pokeapi.co/api/v2/pokemon-species/" + str(i)
                    actionsAllPokemon.append(asyncio.ensure_future(getPokemonData(session, url)))

                result = await asyncio.gather(*actionsAllPokemon)

                for i, pokemonList in enumerate(result):
                    nameFrench = json.loads(json.dumps(result[i]))["names"][4]["name"]
                    if nameFrench == str(form.data.get('pokemon')).capitalize():
                        id = json.loads(json.dumps(result[i]))["id"]
                        return redirect('index', str(id))
        else:
            return redirect('index', str(random.randint(1, 1117)))


def team_pokemon(request):
    return render(request, 'pokedex/team.html')


def colorType(type):
    return {
        "Plante": "#9bcc50",
        "Poison": "#B97FC9",
        "Feu": "#FD7D24",
        "Psy": "#F366B9",
        "Eau": "#4592C4",
        "Glace": "#51C4E7",
        "Roche": "#A38C21",
        "Insecte": "#729F3F",
        "Normal": "#A4ACAF",
        "Combat": "#D56723",
        "Électrik": "#EED535",
        "Fée": "#FDB9E9",
        "Acier": "#9EB7B8",
        "Spectre": "7B62A3",
        "Tenebre": "#707070",
        "Dragon": "#7038F8",
        "Vol": "#659BCF",
        "Sol": "#664024",
    }[type]
