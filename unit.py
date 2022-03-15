import abc
from abc import ABC

import feutils
import item
from item import Item
from item_type import *
from map import Map
import numpy as np


class Unit(ABC):
    def __init__(self, character_code, x, y, level, job_code, hp_max,
                 strength, skill, spd, luck, defense, res, magic, ally,
                 inventory_codes: list, terminal_condition):
        self.terminal_condition = terminal_condition

        self.character_code = character_code
        self.x = x
        self.y = y
        self.level = level
        self.hp_max = hp_max
        self.current_hp = hp_max
        self.strength = strength
        self.magic = magic
        self.skill = skill
        self.speed = spd
        self.luck = luck
        self.defense = defense
        self.res = res

        self.inventory = item.construct_unit_inventory(inventory_codes)

        self.name = feutils.character_name_table(self.character_code)
        self.job = feutils.class_table(job_code)
        self.move = feutils.movement_table(self.job)
        self.terrain_group = feutils.job_terrain_group(self.job)

        if ally:
            self.con = feutils.character_constitution_table(self.name)
        else:
            self.con = feutils.job_constitution_table(self.job)

    def __str__(self):
        return self.name

    def equip_item(self, index):
        self.inventory[0], self.inventory[index] = self.inventory[index], self.inventory[0]

    def get_attack_range(self):
        atk_range = set()

        for i in self.inventory:
            if i.item_type is ItemType.WEAPON or i.item_type is ItemType.TOME:
                item_ranges = list(map(int, i.info['range'].split(',')))
                for r in item_ranges:
                    atk_range.add(r)

        return sorted(list(atk_range))

    def has_consumable(self):
        for i in self.inventory:
            if i.item_type == ItemType.HEAL_CONSUMABLE:
                return True

        return False

    def get_all_consumables(self):
        consums = []
        for i in self.inventory:
            if i.item_type == ItemType.HEAL_CONSUMABLE:
                consums.append(i)

        return consums

    def goto(self, new_x, new_y):
        self.x, self.y = new_x, new_y

    def use_item(self, index):
        inventory_item = self.inventory[index]
        if inventory_item.item_type == ItemType.HEAL_CONSUMABLE:
            self.heal(inventory_item.info['heal_amount'])
            inventory_item.info['uses'] -= 1

            if inventory_item.info['uses'] == 0:
                del self.inventory[index]

            return True

        else:
            return False

    def heal(self, amount):
        self.current_hp = min(self.current_hp + amount, self.hp_max)

    def take_dmg(self, amount):
        self.current_hp -= amount

    @abc.abstractmethod
    def determine_action(self, env, blue_agents, red_agents):
        pass


class RedUnit(Unit):
    def determine_action(self, env, blue_agents, red_agents):
        unit = env.unwrapped.red_team[env.unwrapped.current_unit]
        all_valid_actions = env.unwrapped.get_valid_actions_in_state(encode=False)

        low_health = unit.current_hp / unit.hp_max <= 0.35

        best_action_value = float('-inf')
        best_action = None

        for action in all_valid_actions:
            if low_health:
                action_value = self.low_health_heuristic(unit, action, env)
                if action_value > best_action_value:
                    best_action_value = action_value
                    best_action = action
            else:
                action_value = self.attack_heuristic(unit, action, env)
                if action_value > best_action_value:
                    best_action_value = action_value
                    best_action = action

        return env.unwrapped.encode_single_move(best_action)

    def low_health_heuristic(self, unit, action, env):
        blue_units = env.unwrapped.blue_team
        current_unit = env.unwrapped.red_team[env.unwrapped]
        x, y = action.x, action.y
        closest_blue_unit = self.get_closest_blue_unit(blue_units, unit)
        distance = feutils.manhattan_distance(x, y, closest_blue_unit.x, closest_blue_unit.y)

        attack_factor = 0
        if action.is_attack():
            attack_factor = distance * -9

        return (distance * 10) + attack_factor

    def get_closest_blue_unit(self, blue_units, unit):
        closest_unit = None
        closest_distance = float('inf')
        for blue in blue_units:
            x, y = blue.x, blue.y
            dis = feutils.manhattan_distance(x, y, unit.x, unit.y)
            if dis < closest_distance:
                closest_distance = dis
                closest_unit = blue
        return closest_unit

    def attack_heuristic(self, unit, action, env):
        blue_units = env.unwrapped.blue_team
        current_unit = env.unwrapped.red_team[env.unwrapped]

        return 0


class BlueUnit(Unit):

    def __init__(self, character_code, x, y, level, job_code, hp_max, strength, skill, spd, luck, defense, res, magic,
                 ally, inventory_codes: list, terminal_condition):
        super().__init__(character_code, x, y, level, job_code, hp_max, strength, skill, spd, luck, defense, res, magic,
                         ally, inventory_codes, terminal_condition)

        """
        VERSION_1

        State space is E * N
        where:     
            E : number of enemy units that can attack this unit
            N : health percentage encoded as an integer. 
        """
        self.state_space = np.array([15, 10])

        """
        VERSION_1

        Action space is simply either [0, 1, 2]
        0 - Wait
        1 - Item
        2 - Attack
        """
        self.action_space = np.array([3])

        self.q_table = np.zeros(np.concatenate((self.state_space, self.action_space)))

    def determine_action(self, env, blue_agents, red_agents):
        pass

