import abc
import random
from abc import ABC
import os
import feutils
import item
from item import Item
from item_type import *
from map import Map
import numpy as np
import numpy.ma as npma
import feutils

from environment import Environment


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
            heal_total = self.heal(inventory_item.info['heal_amount'])
            inventory_item.info['uses'] -= 1

            if inventory_item.info['uses'] == 0:
                self.inventory.remove(inventory_item)

            return heal_total

        return None

    def heal(self, amount):
        heal_total = min(amount, self.hp_max - self.current_hp)
        self.current_hp = heal_total
        return heal_total

    def take_dmg(self, amount):
        self.current_hp -= amount

    @abc.abstractmethod
    def determine_action(self, state, env, ally_team, enemy_team):
        pass

    @abc.abstractmethod
    def determine_move(self, action, ally_team, enemy_team, env):
        pass

    @abc.abstractmethod
    def determine_target(self, env, enemy_team):
        pass

    @abc.abstractmethod
    def determine_item_to_use(self, env, enemy_team):
        pass


class RedUnit(Unit):
    def determine_action(self, state, env, ally_team, enemy_team):
        pass

    def determine_move(self, action, ally_team, enemy_team, env):
        pass

    def determine_target(self, env, enemy_team):
        pass

    def determine_item_to_use(self, env, enemy_team):
        pass

    def low_health_heuristic(self, action, env):
        blue_units = env.unwrapped.blue_team
        x, y = action.x, action.y
        closest_blue_unit = self.get_closest_blue_unit(blue_units)
        distance = feutils.manhattan_distance(x, y, closest_blue_unit.x, closest_blue_unit.y)

        attack_factor = 0
        if action.is_attack():
            attack_factor = distance * -9

        return (distance * 10) + attack_factor

    def get_closest_blue_unit(self, blue_units):
        closest_unit = None
        closest_distance = float('inf')
        for blue in blue_units:
            x, y = blue.x, blue.y
            dis = feutils.manhattan_distance(x, y, self.x, self.y)
            if dis < closest_distance:
                closest_distance = dis
                closest_unit = blue
        return closest_unit

    def attack_heuristic(self, action, env):
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
        self._version = "1"

        self.q_table = self.init_q_table()

        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.5

        self.table_name = f'{self.name}_qtable_v{self._version}_{self.alpha}-{self.gamma}-{self.epsilon}.npy'

    def init_q_table(self):
        if not os.path.exists(f'qtables/{self.table_name}'):
            return np.zeros(np.concatenate((self.state_space, self.action_space)))
        else:
            return np.load(self.table_name)

    def close(self):
        np.save(f'qtables/{self.table_name}', self.q_table)

    def update_qtable(self, state, reward, action):
        pass

    def determine_action(self, state, env: Environment, ally_team, enemy_team):
        action_mask = env.generate_action_mask(self, ally_team, enemy_team)
        # copy so when we mask invalid actions it doesn't change q table
        state_action_space = npma.masked_array(self.q_table[state],
                                               fill_value=float('-inf'),
                                               mask=action_mask,
                                               copy=True)

        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(state_action_space.count())
        else:
            action = np.argmax(state_action_space)  # Exploit learned value

        return action  # 0, 1, or 2

    def determine_move(self, action, ally_team, enemy_team, env):
        valid_moves = env.generate_valid_moves(self, ally_team, enemy_team)
        return random.choice(valid_moves)

    def determine_target(self, env, enemy_team):
        attackable_targets = feutils.attackable_units(self, enemy_team)
        return random.choice(attackable_targets)

    def determine_item_to_use(self, env, enemy_team):
        usable_items = self.get_all_consumables()
        return random.choice(usable_items)
