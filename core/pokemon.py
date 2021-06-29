class Pokemon():

    def __init__(
            self, dex_num=0, species='', form='', type1='', type2='', family='',
            base_capture_rate=0, base_flee_rate=0, base_capture_shadow=0, base_flee_shadow=0,
            base_stamina=0, base_attack=0, base_defense=0,
            quick_moves=None, charged_moves=None, legacy_quick_moves=None, legacy_charged_moves=None,
            third_move_dust=0, third_move_candy=0,
            is_tradable=False, buddy_energy=0, mega_evo_energy_init=0, mega_evo_energy_subs=0):
            
        self.dex_num = dex_num
        self.species = species
        self.form = form
        self.type1 = type1
        self.type2 = type2
        self.family = family
        self.base_capture_rate = base_capture_rate
        self.base_flee_rate = base_flee_rate
        self.base_capture_shadow = base_capture_shadow
        self.base_flee_shadow = base_flee_shadow
        self.base_stamina = base_stamina
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.quick_moves = [] if quick_moves is None else quick_moves
        self.charged_moves = [] if charged_moves is None else charged_moves
        self.legacy_quick_moves = [] if legacy_quick_moves is None else legacy_quick_moves
        self.legacy_charged_moves = [] if legacy_charged_moves is None else legacy_charged_moves
        self.third_move_dust = third_move_dust
        self.third_move_candy = third_move_candy
        self.is_tradable = is_tradable
        self.buddy_energy = buddy_energy
        self.mega_evo_energy_init = mega_evo_energy_init
        self.mega_evo_energy_subs = mega_evo_energy_subs