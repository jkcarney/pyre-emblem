import random

from unit import BlueUnit, RedUnit
from map import Map
import numpy as np


class UnitFactory:
    def __init__(self, blue_low, blue_high, red_low, red_high, run_name):
        self.blue_low = blue_low
        self.blue_high = blue_high
        self.red_low = red_low
        self.red_high = red_high
        self.run_name = run_name

    def get_nonterminal_unit_base_stats(self, unit_name):
        character_dict = {
            'Sain': BlueUnit(0xd2f8, 0, 0, 1, 0xe7c, 19, 8, 4, 6, 4, 6, 0, 0, True, [0x14, 0x6b], False, self.run_name),
            'Kent': BlueUnit(0xd2c4, 0, 0, 1, 0xe7c, 20, 6, 6, 7, 2, 5, 1, 0, True, [0x1, 0x6b], False, self.run_name),
            'Florina': BlueUnit(0xd3fc, 0, 0, 1, 0x11c4, 17, 5, 7, 9, 7, 4, 4, 0, True, [0x14, 0x6b], False, self.run_name),
            'Wil': BlueUnit(0xd0f0, 0, 0, 2, 0x93c, 20, 6, 5, 5, 6, 5, 0, 0, True, [0x2c, 0x6b], False, self.run_name),
            'Dorcas': BlueUnit(0xcfb8, 0, 0, 3, 0x744, 30, 7, 7, 6, 3, 3, 0, 0, True, [0x28, 0x6b], False, self.run_name),
            'Erk': BlueUnit(0xd1f4, 0, 0, 1, 0xbdc, 17, 0, 6, 7, 3, 2, 4, 5, True, [0x37, 0x6b], False, self.run_name),
            'Rath': BlueUnit(0xd3c8, 0, 0, 7, 0x1074, 25, 8, 9, 10, 5, 7, 2, 0, True, [0x2c, 0x6b, 0x6b], False, self.run_name),
            'Matthew': BlueUnit(0xd534, 0, 0, 2, 0x150c, 18, 4, 4, 11, 2, 3, 0, 0, True, [0x1, 0x6b], False, self.run_name),
            'Lucius': BlueUnit(0xd158, 0, 0, 3, 0xa8c, 18, 0, 6, 10, 2, 1, 6, 7, True, [0x3e, 0x6b], False, self.run_name),
            'Marcus': BlueUnit(0xd360, 0, 0, 1, 0xf24, 31, 15, 15, 11, 8, 10, 8, 0, True, [0x17, 0x6b], False, self.run_name),
            'Lowen': BlueUnit(0xd32c, 0, 0, 2, 0xe7c, 23, 7, 5, 7, 3, 7, 0, 0, True, [0x1c, 0x6b], False, self.run_name),
            'Rebecca': BlueUnit(0xd0f0, 0, 0, 1, 0x990, 17, 4, 5, 6, 4, 3, 1, 0, True, [0x2c, 0x6b], False, self.run_name),
            'Bartre': BlueUnit(0xcfec, 0, 0, 2, 0x744, 29, 9, 5, 3, 4, 4, 0, 0, True, [0x1f, 0x6b], False, self.run_name),
            'Oswin': BlueUnit(0xd054, 0, 0, 9, 0x7ec, 29, 13, 9, 5, 3, 13, 3, 0, True, [0x14, 0x6c], False, self.run_name),
            'Guy': BlueUnit(0xcf50, 0, 0, 3, 0x5f4, 21, 6, 11, 11, 5, 5, 0, 0, True, [0xd, 0x6c], False, self.run_name),
            'Raven': BlueUnit(0xcee8, 0, 0, 5, 0x4a4, 25, 8, 11, 13, 2, 5, 1, 0, True, [0x3, 0x6c], False, self.run_name),
            'Canas': BlueUnit(0xd290, 0, 0, 8, 0xd2c, 21, 0, 9, 8, 7, 5, 8, 10, True, [0x44, 0x6c], False, self.run_name),
            'Dart': BlueUnit(0xd874, 0, 0, 8, 0x1464, 34, 12, 8, 8, 3, 6, 1, 0, True, [0x20, 0x6c], False, self.run_name),
            'Heath': BlueUnit(0xd498, 0, 0, 7, 0x126c, 28, 11, 8, 7, 7, 10, 1, 0, True, [0x16, 0x6c], False, self.run_name)
        }
        return character_dict[unit_name]

    def get_terminal_unit_base_stats(self, unit_name):
        character_dict = {
            'Lyn': BlueUnit(0xceb4, 0, 0, 1, 0x204, 16, 4, 7, 9, 5, 2, 0, 0, True, [0xa, 0x6c], True, self.run_name),
            'Eliwood': BlueUnit(0xce4c, 0, 0, 1, 0x1b0, 18, 5, 5, 7, 7, 5, 0, 0, True, [0x9, 0x6c], True, self.run_name),
            'Hector': BlueUnit(0xce80, 0, 0, 1, 0x258, 19, 7, 4, 5, 3, 8, 0, 0, True, [0x8d, 0x6c], True, self.run_name)
        }
        return character_dict[unit_name]


    def get_unit_growths(self, unit_name):
        character_dict = {
            'Lyn': np.array([0.70, 0.40, 0.60, 0.60, 0.55, 0.20, 0.30]),
            'Sain': np.array([0.80, 0.60, 0.35, 0.40, 0.35, 0.20, 0.20]),
            'Kent': np.array([0.85, 0.40, 0.50, 0.45, 0.20, 0.25, 0.25]),
            'Florina': np.array([0.60, 0.40, 0.50, 0.55, 0.50, 0.15, 0.35]),
            'Wil': np.array([0.75, 0.50, 0.50, 0.40, 0.40, 0.20, 0.25]),
            'Dorcas': np.array([0.80, 0.60, 0.40, 0.20, 0.45, 0.25, 0.15]),
            'Erk': np.array([0.65, 0.40, 0.40, 0.50, 0.30, 0.20, 0.40]),
            'Rath': np.array([0.80, 0.50, 0.40, 0.50, 0.30, 0.10, 0.25]),
            'Matthew': np.array([0.75, 0.30, 0.40, 0.70, 0.50, 0.25, 0.20]),
            'Lucius': np.array([0.55, 0.60, 0.50, 0.40, 0.20, 0.10, 0.60]),
            'Eliwood': np.array([0.80, 0.45, 0.50, 0.40, 0.45, 0.30, 0.35]),
            'Marcus': np.array([0.65, 0.30, 0.50, 0.25, 0.30, 0.15, 0.35]),
            'Lowen': np.array([0.90, 0.30, 0.30, 0.30, 0.50, 0.40, 0.30]),
            'Rebecca': np.array([0.60, 0.40, 0.50, 0.60, 0.50, 0.15, 0.30]),
            'Bartre': np.array([0.85, 0.50, 0.35, 0.40, 0.30, 0.30, 0.25]),
            'Hector': np.array([0.90, 0.60, 0.45, 0.35, 0.30, 0.50, 0.25]),
            'Oswin': np.array([0.90, 0.40, 0.30, 0.30, 0.35, 0.55, 0.30]),
            'Guy': np.array([0.75, 0.30, 0.50, 0.70, 0.45, 0.15, 0.25]),
            'Raven': np.array([0.85, 0.55, 0.40, 0.45, 0.35, 0.25, 0.15]),
            'Canas': np.array([0.70, 0.45, 0.40, 0.35, 0.25, 0.25, 0.45]),
            'Dart': np.array([0.70, 0.65, 0.20, 0.60, 0.35, 0.20, 0.15]),
            'Heath': np.array([0.80, 0.50, 0.50, 0.45, 0.20, 0.30, 0.20])
        }
        return character_dict[unit_name]

    def generate_random_enemy(self):
        character_code = 0xdab0
        level = random.randint(1, 3)
        hp = random.randint(16, 22)
        power = random.randint(2, 6)
        skill = random.randint(2, 3)
        spd = random.randint(2, 4)
        reduction = random.randint(0, 3)
        secondary_reduction = random.randint(0, 2)
        luck = random.randint(1, 3)

        return random.choice([
            # Mercenary
            RedUnit(character_code, 0, 0, level, 0x4a4, hp, power + 2, skill + 4, spd + 2,
                    luck, reduction, secondary_reduction, 0, False, [0x1], False, self.run_name),
            # Myrmidon
            RedUnit(character_code, 0, 0, level, 0x5f4, hp, power, skill + 3, spd + 4,
                    luck, reduction, secondary_reduction, 0, False, [0x1], False, self.run_name),
            # Fighter
            RedUnit(character_code, 0, 0, level, 0x744, hp, power, skill, spd,
                    luck, reduction, secondary_reduction, 0, False, [0x1f], False, self.run_name),
            # Knight
            RedUnit(character_code, 0, 0, level, 0x7ec, hp, power + 2, skill, spd - 1,
                    luck, reduction + 5, secondary_reduction, 0, False, [0x14], False, self.run_name),
            # Archer
            RedUnit(character_code, 0, 0, level, 0x93c, hp, power, skill + 1, spd + 1,
                    luck, reduction, secondary_reduction, 0, False, [0x2c], False, self.run_name),
            # Mage
            RedUnit(character_code, 0, 0, level, 0xbdc, hp, 0, skill, spd,
                    luck, secondary_reduction, reduction, power, False, [0x37], False, self.run_name),
            # Shaman
            RedUnit(character_code, 0, 0, level, 0xd2c, hp, 0, skill, spd,
                    luck, secondary_reduction + 2, reduction, power, False, [0x44], False, self.run_name),
            # Cavalier w/ lance
            RedUnit(character_code, 0, 0, level, 0xe7c, hp, power + 1, skill + 1, spd + 1,
                    luck, reduction + 1, secondary_reduction + 1, 0, False, [0x14], False, self.run_name),
            # Cavalier w/ sword
            RedUnit(character_code, 0, 0, level, 0xe7c, hp, power + 1, skill + 1, spd + 1,
                    luck, reduction + 1, secondary_reduction + 1, 0, False, [0x1], False, self.run_name),
            # Soldier
            RedUnit(character_code, 0, 0, level, 0x13bc, hp, power - 1, skill - 2, spd - 2,
                    0, max(reduction - 2, 0), max(secondary_reduction - 1, 0), 0, False, [0x14], False, self.run_name),
            # Wyvern Rider
            RedUnit(character_code, 0, 0, level, 0x126c, hp, power + 1, skill, spd,
                    luck, reduction + 1, secondary_reduction, 0, False, [0x14], False, self.run_name),
            # Brigand w/ Iron axe
            RedUnit(character_code, 0, 0, level, 0x1410, hp, power + 1, skill - 1, spd,
                    luck, reduction - 1, secondary_reduction, 0, False, [0x1f], False, self.run_name),
            # Brigand w/ hand axe
            RedUnit(character_code, 0, 0, level, 0x1410, hp, power + 1, skill - 1, spd,
                    luck, reduction - 1, secondary_reduction, 0, False, [0x28], False, self.run_name),
            # Pirate
            RedUnit(character_code, 0, 0, level, 0x1464, hp, power + 1, skill - 2, spd,
                    luck, reduction - 1, secondary_reduction, 0, False, [0x1f], False, self.run_name)

        ])

    def generate_blue_team(self, tile_map: Map):
        """
        We want to place the blue team first on the map

        :param tile_map:
        :return:
        """
        all_non_terminal_units = ['Sain', 'Kent', 'Florina', 'Wil', 'Dorcas', 'Erk', 'Rath', 'Matthew', 'Lucius', 'Marcus',
                                  'Lowen', 'Rebecca', 'Bartre', 'Oswin', 'Guy', 'Raven', 'Canas', 'Dart', 'Heath']
        all_terminal_units = ['Lyn', 'Eliwood', 'Hector']
        deploy = []

        for _ in range(random.randint(self.blue_low, self.blue_high)):
            unit_name = random.choice(all_non_terminal_units)
            all_non_terminal_units.remove(unit_name)
            deploy.append(self.get_nonterminal_unit_base_stats(unit_name))

        lord = self.get_terminal_unit_base_stats(random.choice(all_terminal_units))

        tile_map.set_all_blue_start_coordinates(lord, deploy)

        deploy.append(lord)

        return deploy

    def generate_red_team(self, tile_map: Map, blue_team):
        deploy = []
        for _ in range(random.randint(self.red_low, self.red_high)):
            deploy.append(self.generate_random_enemy())

        for red_unit in deploy:
            tile_map.set_red_unit_start_coordinates(red_unit, deploy, blue_team)

        return deploy
