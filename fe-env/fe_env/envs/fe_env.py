import gym
from gym import error, spaces, utils
from gym.spaces import Space, MultiDiscrete
from gym.utils import seeding

import map_factory
import numpy as np
import map
from action import Action
import combat
from combat import CombatResults, CombatSummary
import unit_populator


class FireEmblemEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(FireEmblemEnvironment, self).__init__()

        self.map_factory = map_factory.OutdoorMapFactory(15, 18, 15, 18)
        self.map, self.number_map = self.map_factory.generate_map()

        self.blue_team = unit_populator.generate_blue_team(self.map)
        self.red_team = unit_populator.generate_red_team(self.map, self.blue_team)

        self.turn_count = 0
        self.turn_limit = 100
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

        self.reward_range = [-100, 100]
        self.action_space = MultiDiscrete([
            self.map.x,  # represents x coordinate of move
            self.map.y,  # represents y coordinate of move
            3,  # represents either Wait(0), Item(1), or Attack(2)
            max(5, len(self.blue_team), len(self.red_team))  # represents the action item of the action above.
            # if the action is zero, then this argument doesn't matter.
            # If the action is one, this represents the index of the item to use
            # If the action is two, this represents the index of the enemy
            # unit to attack
        ])
        self.observation_space = MultiDiscrete([self.map.x, self.map.y])

    def __num_to_action_name(self, n):
        action_map = {0: 'Wait', 1: 'Item', 2: 'Attack'}
        return action_map[n]

    def __action_name_to_num(self, action):
        action_map = {'Wait': 0, 'Item': 1, 'Attack': 2}
        return action_map[action]

    def parse_action_from_action_space(self, raw_action):
        action_name = self.__num_to_action_name(raw_action[2])
        x, y = raw_action[0], raw_action[1]

        if self.current_phase == 'Blue':
            if action_name == 'Attack':
                action_item = self.red_team[raw_action[3]]
            elif action_name == 'Item':
                action_item = self.blue_team[self.current_unit].inventory[raw_action[3]]
            else:
                action_item = None
        else:
            if action_name == 'Attack':
                action_item = self.blue_team[raw_action[3]]
            elif action_name == 'Item':
                action_item = self.red_team[self.current_unit].inventory[raw_action[3]]
            else:
                action_item = None

        return Action(action_name, action_item, x, y)

    def step(self, raw_action):
        action = self.parse_action_from_action_space(raw_action)

        if self.current_phase == 'Blue':
            self.__blue_phase(action)
            self.current_unit += 1

            if self.current_unit >= len(self.blue_team):
                self.current_phase = 'Red'
                self.current_unit = 0
                print('-- RED PHASE --')

        elif self.current_phase == 'Red':
            self.__red_phase(action)
            self.current_unit += 1

            if self.current_unit >= len(self.red_team):
                self.current_phase = 'Blue'
                self.current_unit = 0
                self.turn_count += 1
                print(f'-- TURN {self.turn_count} --')
                print('-- BLUE PHASE --')

        if self.turn_count == self.turn_limit:
            self.red_victory = True

        done = False
        reward = 0

        # return observation, reward, done, info
        if self.red_victory:
            done = True
            reward = -100

        if self.blue_victory:
            done = True
            reward = 100

        return None, reward, done, {}

    def get_valid_actions_in_state(self, encode=True):
        if self.current_phase == 'Blue':
            unit = self.blue_team[self.current_unit]
            valid_coordinates = self.map.get_valid_move_coordinates(unit, self.blue_team, self.red_team)
            non_encoded_moves = self.map.get_all_valid_actions(unit, self.red_team, valid_coordinates)
        else:
            unit = self.red_team[self.current_unit]
            valid_coordinates = self.map.get_valid_move_coordinates(unit, self.red_team, self.blue_team)
            non_encoded_moves = self.map.get_all_valid_actions(unit, self.blue_team, valid_coordinates)

        if encode:
            return self.encode_moves(non_encoded_moves)
        else:
            return non_encoded_moves

    def encode_moves(self, non_encoded_moves):
        encoded_moves = []

        for move in non_encoded_moves:
            encoded_move = self.encode_single_move(move)
            encoded_moves.append(encoded_move)

        return encoded_moves

    def encode_single_move(self, move):
        encoded_name = self.__action_name_to_num(move.name)
        x, y = move.x, move.y
        if move.name == 'Attack':
            if self.current_phase == 'Blue':
                encoded_action_item = self.red_team.index(move.action_item)
            else:
                encoded_action_item = self.blue_team.index(move.action_item)

        elif move.name == 'Item':
            if self.current_phase == 'Blue':
                encoded_action_item = self.blue_team[self.current_unit].inventory.index(move.action_item)
            else:
                encoded_action_item = self.red_team[self.current_unit].inventory.index(move.action_item)

        else:
            encoded_action_item = 0

        return np.array([x, y, encoded_name, encoded_action_item])

    def __blue_phase(self, action_choice):
        unit = self.blue_team[self.current_unit]
        x, y = action_choice.x, action_choice.y
        unit.goto(x, y)
        print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")

        if action_choice.is_attack():
            # Defender in this case is from self.enemies
            defender = action_choice.action_item
            combat_stats = combat.get_combat_stats(unit, defender, self.map)
            result = combat.simulate_combat(combat_stats)
            print(f"\t {result.name}")

            if result is CombatResults.DEFENDER_DEATH:
                self.red_team.remove(defender)
                if not self.red_team:
                    self.blue_victory = True

            elif result is CombatResults.ATTACKER_DEATH:
                if unit.terminal_condition:
                    self.red_victory = True
                self.blue_team.remove(unit)

        elif action_choice.is_item():
            item_to_use = action_choice.action_item
            heal_amount = item_to_use.info['heal_amount']
            unit.heal(heal_amount)
            item_to_use.info['uses'] -= 1
            if item_to_use.info['uses'] == 0:
                unit.inventory.remove(item_to_use)

    def __red_phase(self, action_choice):
        unit = self.red_team[self.current_unit]
        x, y = action_choice.x, action_choice.y
        unit.goto(x, y)
        print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")

        if action_choice.is_attack():
            # Defender in this case is from self.enemies
            defender = action_choice.action_item
            combat_stats = combat.get_combat_stats(unit, defender, self.map)
            result = combat.simulate_combat(combat_stats)
            print(f"\t {result.name}")

            if result is CombatResults.DEFENDER_DEATH:
                if defender.terminal_condition:
                    self.red_victory = True
                self.blue_team.remove(defender)

            elif result is CombatResults.ATTACKER_DEATH:
                self.red_team.remove(unit)
                if not self.red_team:
                    self.blue_victory = True

        elif action_choice.is_item():
            item_to_use = action_choice.action_item
            heal_amount = item_to_use.info['heal_amount']
            unit.heal(heal_amount)
            item_to_use.info['uses'] -= 1
            if item_to_use.info['uses'] == 0:
                unit.inventory.remove(item_to_use)

    def reset(self):
        self.map_factory = map_factory.OutdoorMapFactory(15, 20, 15, 20)
        self.map, self.number_map = self.map_factory.generate_map()

        self.blue_team = unit_populator.generate_blue_team(self.map)
        self.red_team = unit_populator.generate_red_team(self.map, self.blue_team)

        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

        self.action_space = MultiDiscrete([
            self.map.x,  # represents x coordinate of move
            self.map.y,  # represents y coordinate of move
            3,  # represents either Wait(0), Item(1), or Attack(2)
            max(5, len(self.blue_team), len(self.red_team))
            # represents the action item of the action above:

            # if the action is zero, then this argument doesn't matter.
            # If the action is one, this represents the index of the item to use
            # If the action is two, this represents the index of the enemy
            # unit to attack
        ])
        self.observation_space = MultiDiscrete([self.map.x, self.map.y])

    def render(self, mode="human"):
        pass

    def close(self):
        pass
