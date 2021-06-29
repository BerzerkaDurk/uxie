import json
from os import name
import discord
from discord.ext import commands

from core import checks

def _unpack_forms():
    with open('data/latest.json') as f:                     #open game master
        data = json.load(f)
    form_list = []
    pokemon_template = {'dex_num': None, 'species': '', 'candy_per_xl': 0,
               'forms': [{'form': None, 'template_id': None, 'male_percent': 0, 'female_percent': 0}],
               'mega_form': None}
    for i in range(len(data)):
        pokemon = pokemon_template.copy()
        if data[i]['templateId'].startswith('FORMS'):
            pokemon['dex_num'] = int(data[i]['templateId'][7:11])
            pokemon['species'] = data[i]['templateId'].split('_',4)[3]
            if len(pokemon['species']) == 2:
                pokemon['species'] += '_' + data[i]['templateId'].split('_', 5)[4]
            pokemon['forms'] = []
            if 'forms' in data[i]['data']['formSettings']:
                for j in range(len(data[i]['data']['formSettings']['forms'])):
                    if data[i]['data']['formSettings']['forms'][j]['form'].split('_')[-1] == 'PURIFIED':
                        continue
                    elif 'isCostume' in data[i]['data']['formSettings']['forms'][j]:
                        if data[i]['data']['formSettings']['forms'][j]['isCostume'] == 'true':
                            continue
                    else:
                        form = data[i]['data']['formSettings']['forms'][j]['form'][len(pokemon['species']) + 1:]
                        pokemon['forms'].append(form)
            if pokemon['forms'] == []:
                pokemon['forms'] = ['']
            form_list.append(pokemon.copy())
    with open('data/forms.json', 'w') as write_file:
        json.dump(form_list, write_file, indent=4)
    return(True)

def _unpack_families():
    with open('data/latest.json') as f:
        data = json.load(f)
    family_list = []
    family = {'family': None, 'candy_per_xl': None, 'mega_form': None}
    for i in range(len(data)):
        family['family'] = None
        family['candy_per_xl'] = None
        family['mega_form'] = None
        if 'FAMILY' in data[i]['templateId'].split('_'):
            if 'data' in data[i]:
                if 'pokemonFamily' in data[i]['data']:
                    if 'familyId' in data[i]['data']['pokemonFamily']:
                        family['family'] = data[i]['data']['pokemonFamily']['familyId']
                    if 'candyPerXlCandy' in data[i]['data']['pokemonFamily']:
                        family['candy_per_xl'] = data[i]['data']['pokemonFamily']['candyPerXlCandy']
                    if 'megaEvolvablePokemonId' in data[i]['data']['pokemonFamily']:
                        family['mega_form'] = data[i]['data']['pokemonFamily']['megaEvolvablePokemonId']
            family_list.append(family.copy())
    with open('data/families.json', 'w') as write_file:
        json.dump(family_list, write_file, indent= 4)

def _unpack_spawns():
    with open('data/forms.json', 'r') as f:
        forms = json.load(f)
    with open('data/latest.json', 'r') as f:
        data = json.load(f)
    spawn_list = []
    spawn = {'species': None, 'form': None, 'template_id': None, 'percent_male': 0, 'percent_female': 0}
    for record in forms:
        for form in record['forms']:
            search = 'SPAWN_V' + str(record['dex_num']).zfill(4) + '_POKEMON_' + record['species'] + '_' + form
            if form == '':
                search = search[:-1]
            for i in range(len(data)):
                if data[i]['templateId'] == search:
                    spawn['species'] = record['species']
                    spawn['form'] = form
                    spawn['template_id'] = search[6:]
                    if not 'genderlessPercent' in data[i]['data']['genderSettings']['gender']:
                        if 'malePercent' in data[i]['data']['genderSettings']['gender']:
                            spawn['percent_male'] = data[i]['data']['genderSettings']['gender']['malePercent']
                        if 'femalePercent' in data[i]['data']['genderSettings']['gender']:
                            spawn['percent_female'] = data[i]['data']['genderSettings']['gender']['femalePercent']
                    spawn_list.append(spawn.copy())
                    spawn['percent_male'] = 0
                    spawn['percent_female'] = 0
    with open('data/spawns.json', 'w') as write_file:
        json.dump(spawn_list, write_file, indent= 4)


class Unpack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def unpack(self, ctx):
        _unpack_forms()
        _unpack_families()
        _unpack_spawns()

def setup(bot):
    bot.add_cog(Unpack(bot))