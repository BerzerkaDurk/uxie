import json
import discord
from discord.ext import commands

from core import checks

class Update(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def update(self, ctx):
        
        with open('data/latest.json') as f:                     #open game master
            data = json.load(f)

        temp_data = []                                          #extract list of pokemon
        for i in range(len(data)):
            if data[i]['templateId'].startswith('SPAWN'):
                temp_data.append(data[i]['templateId'][6:])

        f = open('data/masterdata.csv', 'w')                     #overwrite current file and add headers
        f.write('dexnumber, species, form, type1, type2, base catch rate, base flee rate, stamina, attack, defense, quick moves, charge moves, elite quick moves, elite charge moves, third move dust, third move candy, purify dust, purify candy\n')
        f.close()
        for i in range(len(data)):
            if data[i]['templateId'] in temp_data:
                id = data[i]['templateId'].split('_', 3)
                dex_num = int(id.pop(0)[1:])
                species = id[1]
                if len(id) == 3:
                    if species == "MR":                         #exception for Mr. Mime and Mr. Rime
                        species += '_' + id[2][:4]
                        form = id[2][5:]
                    else:
                        form = id[2]
                else:
                    form = ""
                if 'pokemonSettings' in data[i]['data']:
                    type = data[i]['data']['pokemonSettings']['type']
                    if 'type2' in data[i]['data']['pokemonSettings']:
                        type2 = data[i]['data']['pokemonSettings']['type2']
                    else:
                        type2 = ""
                    if 'encounter' in data[i]['data']['pokemonSettings']:
                        if 'baseCaptureRate' in data[i]['data']['pokemonSettings']['encounter']:
                            base_capture_rate = data[i]['data']['pokemonSettings']['encounter']['baseCaptureRate']
                        else:
                            base_capture_rate = ""
                        if 'baseFleeRate' in data[i]['data']['pokemonSettings']['encounter']:
                            base_flee_rate = data[i]['data']['pokemonSettings']['encounter']['baseFleeRate']
                        else:
                            base_flee_rate = ""
                    else:
                        base_capture_rate, base_flee_rate = ""
                    if 'stats' in data[i]['data']['pokemonSettings']:
                        if 'baseStamina' in data[i]['data']['pokemonSettings']['stats']:
                            base_stamina = data[i]['data']['pokemonSettings']['stats']['baseStamina']
                        else:
                            base_stamina = ""
                        if 'baseAttack' in data[i]['data']['pokemonSettings']['stats']:
                            base_attack = data[i]['data']['pokemonSettings']['stats']['baseAttack']
                        else:
                            base_attack = ""
                        if 'baseDefense' in data[i]['data']['pokemonSettings']['stats']:
                            base_defense = data[i]['data']['pokemonSettings']['stats']['baseDefense']
                        else:
                            base_defense = ""
                    else:
                        base_stamina, base_attack, base_defense = ""
                    quick_moves = ""
                    if 'quickMoves' in  data[i]['data']['pokemonSettings']:
                        for move in data[i]['data']['pokemonSettings']['quickMoves']:
                            quick_moves += move + ' '
                        quick_moves = quick_moves[:-1]
                    charge_moves = ""
                    if 'cinematicMoves' in data[i]['data']['pokemonSettings']:
                        for move in data[i]['data']['pokemonSettings']['cinematicMoves']:
                            charge_moves += move + ' '
                        charge_moves = charge_moves[:-1]
                    legacy_quick_moves = ""
                    if 'eliteQuickMove' in  data[i]['data']['pokemonSettings']:
                        for move in data[i]['data']['pokemonSettings']['eliteQuickMove']:
                            legacy_quick_moves += move + ' '
                        legacy_quick_moves = legacy_quick_moves[:-1]
                    legacy_charge_moves = ""
                    if 'eliteCinematicMove' in data[i]['data']['pokemonSettings']:
                        for move in data[i]['data']['pokemonSettings']['eliteCinematicMove']:
                            legacy_charge_moves += move + ' '
                        legacy_charge_moves = legacy_charge_moves[:-1]
                    if 'thirdMove' in data[i]['data']['pokemonSettings']:
                        if 'stardustToUnlock' in data[i]['data']['pokemonSettings']['thirdMove']:
                            third_move_dust = data[i]['data']['pokemonSettings']['thirdMove']['stardustToUnlock']
                        else:
                            third_move_dust = ""
                        if 'candyToUnlock' in data[i]['data']['pokemonSettings']['thirdMove']:
                            third_move_candy = data[i]['data']['pokemonSettings']['thirdMove']['candyToUnlock']
                        else:
                            third_move_candy = ""
                    else:
                        third_move_dust, third_move_candy = ""
                    if 'shadow' in data[i]['data']['pokemonSettings']:
                        if 'purificationStardustNeeded' in data[i]['data']['pokemonSettings']['shadow']:
                            purify_dust = data[i]['data']['pokemonSettings']['shadow']['purificationStardustNeeded']
                        else:
                            purify_dust = ""
                        if 'purificationCandyNeeded' in data[i]['data']['pokemonSettings']['shadow']:
                            purify_candy = data[i]['data']['pokemonSettings']['shadow']['purificationCandyNeeded']
                        else:
                            purify_candy = ""
                    else:
                        purify_dust = ""
                        purify_candy = ""
                else:
                    type, type2, base_capture_rate, base_flee_rate, base_stamina, base_attack = ""
                    base_defense, third_move_dust, third_move_candy = ""
                    quick_moves, charge_moves, legacy_quick_moves, legacy_charge_moves = ""
                f = open('data/masterdata.csv', 'a')
                f.write(f'{dex_num},{species},{form},{type},{type2},{base_capture_rate},')
                f.write(f'{base_flee_rate}, {base_stamina}, {base_attack}, {base_defense}, {quick_moves},')
                f.write(f'{charge_moves}, {legacy_quick_moves}, {legacy_charge_moves}, {third_move_dust},')
                f.write(f'{third_move_candy}, {purify_dust}, {purify_candy}\n')
                f.close()
                if form == "" and 'tempEvoOverrides' in data[i]['data']['pokemonSettings']:
                    for j in range(len(data[i]['data']['pokemonSettings']['tempEvoOverrides'])):
                        form = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['tempEvoId'][15:]
                        if 'stats' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]:
                            if 'baseStamina' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']:
                                base_stamina = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']['baseStamina']
                            else:
                                base_stamina = ""
                            if 'baseAttack' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']:
                                base_attack = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']['baseAttack']
                            else:
                                base_attack = ""
                            if 'baseDefense' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']:
                                base_defense = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['stats']['baseDefense']
                            else:
                                base_defense = ""
                        if 'typeOverride1' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]:
                            type = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['typeOverride1']
                        if 'typeOverride2' in data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]:
                            type2 = data[i]['data']['pokemonSettings']['tempEvoOverrides'][j]['typeOverride2']   
                        f = open('data/masterdata.csv', 'a')
                        f.write(f'{dex_num},{species},{form},{type},{type2},{base_capture_rate},')
                        f.write(f'{base_flee_rate}, {base_stamina}, {base_attack}, {base_defense}, {quick_moves},')
                        f.write(f'{charge_moves}, {legacy_quick_moves}, {legacy_charge_moves}, {third_move_dust},')
                        f.write(f'{third_move_candy}, {purify_dust}, {purify_candy}\n')
                        f.close()

        await ctx.send(f'Base stats for Pokémon imported successfully.')

def setup(bot):
    bot.add_cog(Update(bot))
