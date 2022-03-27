import abc
import random
from abc import ABC
import os

import combat
import feutils
import item
from item import Item
from item_type import *
from map import Map
import numpy as np
import numpy.ma as npma
import feutils
from feutils import FEAttackRangeError
from termcolor import colored


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
        heal_total = min(self.hp_max - self.current_hp, amount)

        self.current_hp += amount
        if self.current_hp > self.hp_max:
            self.current_hp = self.hp_max

        return heal_total

    def take_dmg(self, amount):
        if amount < 0:
            return
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

    @abc.abstractmethod
    def close(self):
        pass


class RedUnit(Unit):
    def determine_action(self, state, env, ally_team, enemy_team):
        health_percent = self.current_hp / self.hp_max
        consumable_count = len(self.get_all_consumables())
        if health_percent <= 0.35 and consumable_count > 0:
            return 1

        action_mask = env.generate_action_mask(self, ally_team, enemy_team)
        if not action_mask[2]:  # If action_mask[2] is false, that means the unit can attack! So do it
            return 2

        return 0  #

    def determine_move(self, action, ally_team, enemy_team, env):
        valid_moves = env.generate_valid_moves(action, self, ally_team, enemy_team)
        choice = random.choice(valid_moves)
        return choice

    def determine_target(self, env, enemy_team):
        attackable_targets = feutils.attackable_units(self, enemy_team)
        if len(attackable_targets) == 0:
            raise FEAttackRangeError(f"No units were in attack range of {self.name} at coordinate {self.x},{self.y}")

        return random.choice(attackable_targets)

    def determine_item_to_use(self, env, enemy_team):
        usable_items = self.get_all_consumables()
        return random.randrange(len(usable_items))

    def close(self):
        return False


class BlueUnit(Unit):
    def __init__(self, character_code, x, y, level, job_code, hp_max, strength, skill, spd, luck, defense, res, magic,
                 ally, inventory_codes: list, terminal_condition):
        super().__init__(character_code, x, y, level, job_code, hp_max, strength, skill, spd, luck, defense, res, magic,
                         ally, inventory_codes, terminal_condition)

        self._version = "2"

        self.state_space = np.array([10, 10])
        self.action_space = np.array([3])

        # RL hyper-parameters
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.6    # Discount rate
        self.epsilon = 0.1  # Exploration rate; how often do we explore vs exploit

        # Heuristic hyper-parameters
        self.tau = 0.9      # Used in combat heuristic: how much do we care about enemy combat stats vs our own?

        self.table_name = f'{self.name}_qtable_v{self._version}_{self.alpha}-{self.gamma}.npy'

        self.q_table = self.init_q_table()

    def init_q_table(self):
        """
        Either loads q-table on disk if it exists or creates a new one

        :return: a q-table (nd array that is 15x10x3)
        """
        if not os.path.exists(f'qtables/{self.table_name}'):
            return np.zeros(np.concatenate((self.state_space, self.action_space)))
        else:
            return np.load(f'qtables/{self.table_name}')

    def close(self):
        """
        Saves the current state of the q-table to disk.
        Call this AFTER LEARNING!

        :return:
        """
        np.save(f'qtables/{self.table_name}', self.q_table)
        return True

    def update_qtable(self, state, next_state, reward, action):
        """
        Updates q-table greedily using q-learning algorithm.
        Q(s,a) <- Q(s,a) + α[R + γ max(Q(s, a)) - Q(s,a)]

        :param next_state:
        :param state:
        :param reward:
        :param action:
        :return:
        """
        state_action = state + (action,)

        qmax = np.max(self.q_table[next_state])
        current = self.q_table[state_action]

        new_value = current + self.alpha * (reward + (self.gamma * qmax) - current)
        self.q_table[state_action] = new_value

    def determine_action(self, state, env, ally_team, enemy_team):
        """
        Given a state and the environment, determine what action should be taken.
        This will either be exploiting the learned Q-table value or exploration

        :param state: The state as a tuple of ints (ie, 5,6)
        :param env:  The environment object
        :param ally_team: A list of units allied to self
        :param enemy_team: A list of unit that are adversarial to self
        :return: 0, 1, or 2
            0 -> Wait
            1 -> Item
            2 -> Attack
        """

        # Mask invalid Q-Table entries (actions that cannot be taken given the state of the environment)
        # They will be masked as -inf and will not be selectable by get_random_unmasked_action or argmax
        action_mask = env.generate_action_mask(self, ally_team, enemy_team)
        state_action_space = npma.masked_array(self.q_table[state],
                                               fill_value=float('-inf'),
                                               mask=action_mask,
                                               copy=True)

        if np.random.uniform(0, 1) < self.epsilon:
            action = feutils.get_random_unmasked_action(state_action_space)  # Explore action space
            text = colored('(EXPLORE)', 'yellow')
            print(f'{self.name} chose {action} {text}')
        else:
            action = np.argmax(state_action_space)  # Exploit learned value
            text = colored('(EXPLOIT)', 'magenta')
            print(f'{self.name} chose {action} {text}')

        return action  # 0, 1, or 2

    def determine_move(self, action, ally_team, enemy_team, env):
        """
        Given an action that this unit wishes to take, determine the coordinate that this unit should move to that
        would maximize a heuristic.

        The coordinate generated by this function is guaranteed to be valid; the unit (self) is able to move to that
        coordinate and can do that action at that coordinate.

        :param action: The action the unit would take (0, 1, or 2)
        :param ally_team: The team allied to self
        :param enemy_team: The adversarial team to self
        :param env: The environment of the game
        :return: A tuple representing a x,y pair to move to on the grid.
        """
        valid_moves = env.generate_valid_moves(action, self, ally_team, enemy_team)
        choice = random.choice(valid_moves)
        print(f'{self.name} is moving to {str(choice)}')
        return choice

    def determine_target(self, env, enemy_team):
        """
        Determine which unit to attack in this unit's attack range.
        NOTE: when this method is called it is assumed the unit is already moved to the tile that they will attack from
        If they are at a tile where they can attack no enemy units, an FEAttackRangeError will be raised.

        :param env:
        :param enemy_team:
        :except FEAttackRangeError if no enemy units could be attacked from the current position
        :return: A Unit object that self will attack
        """
        def combat_heuristic(enemy_unit):
            """
            A justification for this algorithm will be found in 'research/algorithms.md'
            :param enemy_unit:
            :return: A heuristic of self fighting enemy_unit
            """
            summary = combat.get_combat_stats(self, enemy_unit, env.map)
            ha, hd = summary.attacker_summary.hit_chance, summary.defender_summary.hit_chance
            ma, md = summary.attacker_summary.might, summary.defender_summary.might
            ca, cd = summary.attacker_summary.crit_chance, summary.defender_summary.crit_chance
            da, dd = int(summary.attacker_summary.doubling), int(summary.defender_summary.doubling)

            return (da + 1) * (ma * ha + ma * ca) - self.tau * ((da + 1) * (md * hd + md * cd))

        attackable_targets = feutils.attackable_units(self, enemy_team)
        if len(attackable_targets) == 0:
            raise FEAttackRangeError(f"No units were in attack range of {self.name} at coordinate {self.x},{self.y}")
        attackable_targets.sort(key=combat_heuristic, reverse=True)  # Sort list based on heuristic
        return attackable_targets[0]  # Get biggest value from that heuristic sort

    def determine_item_to_use(self, env, enemy_team):
        usable_items = self.get_all_consumables()
        i = random.choice(usable_items)
        return self.inventory.index(i)
