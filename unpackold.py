import json
from os import name
import discord
from discord.ext import commands

from core import checks

class Unpack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def unpack(self, ctx):
        with open('data/latest.json') as f:                     #open game master
            data = json.load(f)

        temp_data = []                                          #extract list of pokemon
        for i in range(len(data)):
            if data[i]['templateId'].startswith('SPAWN'):
                name_string = data[i]['templateId'].split('_', 4)       #split spawn record into max 4 pieces
                dex_num = int(name_string[1][1:])
                if name_string[3] == 'MR':
                    name_string[3] += '_' + name_string[4][:4]
                    name_string[4] = name_string[4][5:]
                    if name_string[4] == '':
                        name_string[4] = []
                if name_string[3] == 'HO':
                    name_string[3] += '_' + name_string[4][:3]
                    name_string[4] = name_string[4][4:]
                    if name_string[4] == '':
                        name_string[4] = []                    
                species = name_string[3]
                if len(name_string) <= 4:
                    name_string.append([])
                form = name_string[4]
                temp_data.append([dex_num, species, form])

        new_list = [[temp_data[0][0], temp_data[0][1], [temp_data[0][2]], 'False']]
        j = 0
        forms = []
        can_be_shadow = 'False'
        for i in range(1, len(temp_data)):
            if temp_data[i][1] == new_list[j][1]:
                if temp_data[i][2] in ['NORMAL', 'PURIFIED', 'SHADOW']:
                    can_be_shadow = 'True'
                    continue
                forms.append(temp_data[i][2])
                new_list[j][2] = forms
                continue
            new_list[j].append(can_be_shadow)
            new_list.append(temp_data[i])
            can_be_shadow = 'False'
            forms = []
            j += 1

        for record in new_list:
            key_value = str(record[0] / 10000 + .00001)
            key_value = f'V{key_value[2:6]}_POKEMON_{record[1]}'
            for i in range(len(data)):
                if data[i]['templateId'] == key_value:
                    dex_num = record[0]
                    species = record[1].capitalize()
                    if 'data' in data[i]:
                        if 'pokemonSettings' in data[i]['data']:
                            if 'type' in data[i]['data']['pokemonSettings']:
                                type1 = data[i]['data']['pokemonSettings']['type']
                            else:
                                type1 = None
                            if 'type2' in data[i]['data']['pokemonSettings']:
                                type2 = data[i]['data']['pokemonSettings']['type2']
                            else:
                                type2 = None
                            if 'encounter' in data[i]['data']['pokemonSettings']:
                                if 'baseCaptureRate' in data[i]['data']['pokemonSettings']['encounter']:
                                    base_capture_rate = data[i]['data']['pokemonSettings']['encounter']['baseCaptureRate']
                                else:
                                    base_capture_rate = None
                                if 'baseFleeRate' in data[i]['data']['pokemonSettings']['encounter']:
                                    base_flee_rate = data[i]['data']['pokemonSettings']['encounter']['baseFleeRate']
                                else:
                                    base_flee_rate = None
                            else:
                                base_capture_rate, base_flee_rate = None
                            if 'stats' in data[i]['data']['pokemonSettings']:
                                if 'baseStamina' in data[i]['data']['pokemonSettings']['stats']:
                                    base_stamina = data[i]['data']['pokemonSettings']['stats']['baseStamina']
                                else:
                                    base_stamina = None
                                if 'baseAttack' in data[i]['data']['pokemonSettings']['stats']:
                                    base_attack = data[i]['data']['pokemonSettings']['stats']['baseAttack']
                                else:
                                    base_attack = None
                                if 'baseDefense' in data[i]['data']['pokemonSettings']['stats']:
                                    base_defense = data[i]['data']['pokemonSettings']['stats']['baseDefense']
                                else:
                                    base_defense = None
                            else:
                                base_stamina, base_attack, base_defense = None
                            quick_moves = ''
                            if 'quickMoves' in data[i]['data']['pokemonSettings']:
                                for move in data[i]['data']['pokemonSettings']['quickMoves']:
                                    quick_moves += move + ' '
                                    quick_moves = quick_moves[:-1]
                            charged_moves = ''
                            if 'cinematicMoves' in data[i]['data']['pokemonSettings']:
                                for move in data[i]['data']['pokemonSettings']['cinematicMoves']:
                                    charged_moves += move + ' '
                                    charged_moves = charged_moves[:-1]
                            legacy_quick_moves = ''
                            if 'eliteQuickMove' in data[i]['data']['pokemonSettings']:
                                for move in data[i]['data']['pokemonSettings']['eliteQuickMove']:
                                    legacy_quick_moves += move + ' '
                                    legacy_quick_moves = legacy_quick_moves[:-1]
                            legacy_charged_moves = ''
                            if 'eliteCinematicMove' in data[i]['data']['pokemonSettings']:
                                for move in data[i]['data']['pokemonSettings']['eliteCinematicMove']:
                                    legacy_charged_moves += move + ' '
                                    legacy_charged_moves = legacy_charged_moves[:-1]
                            if 'kmBuddyDistance' in data[i]['data']['pokemonSettings']:
                                buddy_distance = data[i]['data']['pokemonSettings']['kmBuddyDistance']                                
                            if 'thirdMove' in data[i]['data']['pokemonSettings']:
                                if 'stardustToUnlock' in data[i]['data']['pokemonSettings']['thirdMove']:
                                    third_move_dust = data[i]['data']['pokemonSettings']['thirdMove']['stardustToUnlock']
                                else:
                                    third_move_dust = None
                                if 'candyToUnlock' in data[i]['data']['pokemonSettings']['thirdMove']:
                                    third_move_candy = data[i]['data']['pokemonSettings']['thirdMove']['candyToUnlock']
                                else:
                                    third_move_candy = None
                            else:
                                 third_move_dust, third_move_candy = None
                            if 'isTradable' in data[i]['data']['pokemonSettings']:
                                is_tradable = data[i]['data']['pokemonSettings']['isTradable']
                            else:
                                is_tradable = None
                            if 'buddyWalkedMegaEnergyAward' in data[i]['data']['pokemonSettings']:
                                buddy_mega_energy = data[i]['data']['pokemonSettings']['buddyWalkedMegaEnergyAward']
                            else:
                                buddy_mega_energy = None
                        else:
                            type1, type2, base_capture_rate, base_flee_rate = None
                            base_stamina, base_attack, base_defense = None
                            quick_moves, charged_moves, legacy_quick_moves, legacy_charged_moves = ''
                            buddy_distance, third_move_dust, third_move_candy, buddy_mega_energy, is_tradable = None

                    f = open('data/masterdata.csv', 'a')
                    f.write(f'{dex_num},{species},{form},{type1},{type2},{base_capture_rate},')
                    f.write(f'{base_flee_rate}, {base_stamina}, {base_attack}, {base_defense}, {quick_moves},')
                    f.write(f'{charged_moves}, {legacy_quick_moves}, {legacy_charged_moves}, {buddy_distance},')
                    f.write(f'{third_move_dust}, {third_move_candy}, {buddy_mega_energy}, {is_tradable}\n') #{purify_dust}, {purify_candy}\n')
                    f.close()

            
        print(species)

def setup(bot):
    bot.add_cog(Unpack(bot))