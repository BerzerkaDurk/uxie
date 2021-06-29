import json
from discord.ext import commands

from core import checks

class Unpack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def unpack(self, ctx):
        with open('data/latest.json', 'r') as f:
            master = json.load(f)
        form_list = []
        pokemon_template = {'dex_num': None, 'species': '', 'candy_per_xl': 0,
                            'forms': [], 'mega_form': False}
        form_template = {'form': None, 'template_id': None, 'male_percent': 0, 'female_percent': 0}
        poke_list = [template for template in master if template['templateId'].startswith('FORMS')]
        for record in poke_list:
            pokemon = pokemon_template.copy()
            pokemon['dex_num'] = int(record['templateId'][7:11])            
            pokemon['species'] = record['templateId'].split('_',4)[3]
            if len(pokemon['species']) == 2:                                        
                pokemon['species'] += '_' + record['templateId'].split('_', 5)[4]
            pokemon['forms'] = []
            if 'forms' in record['data']['formSettings']:
                for j in range(len(record['data']['formSettings']['forms'])):
                    form = form_template.copy()
                    if record['data']['formSettings']['forms'][j]['form'].split('_')[-1] == 'PURIFIED':
                        continue
                    elif 'isCostume' in record['data']['formSettings']['forms'][j]:
                        if record['data']['formSettings']['forms'][j]['isCostume'] == 'true':
                            continue
                    else:
                        form['form'] = record['data']['formSettings']['forms'][j]['form'][len(pokemon['species']) + 1:]
                        form['template_id'] = record['templateId'][6:] + '_' + form['form']
                        pokemon['forms'].append(form)
            else:
                form['form'] = ''
                pokemon['forms'].append(form)
            form_list.append(pokemon.copy())
            




        with open('data/forms.json', 'w') as f:
            json.dump(form_list, f, indent= 4)


def setup(bot):
    bot.add_cog(Unpack(bot))