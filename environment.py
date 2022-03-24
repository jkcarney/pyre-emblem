import math

import feutils
import map_factory
import combat
from combat import CombatResults
import numpy as np


class Environment:
    def __init__(self):
        self.map_factory = map_factory.OutdoorMapFactory(15, 20, 15, 20)
        self.map, self.number_map = self.map_factory.generate_map()

        self.turn_count = 0
        self.turn_limit = 100
        self.blue_victory = False
        self.red_victory = False

    def obtain_state(self, unit, ally_team, enemy_team):
        """
        Obtains the state of the given unit, given the unit's allied and enemy team

        :param unit: The unit whose state we will check
        :param ally_team: The team allied to this unit
        :param enemy_team: The adversarial team to this unit
        :return: state -> a tuple that represents the state (ie, 5,6) (E,N)
        state[0] (E) represents the number of enemies that can attack this unit if they wanted to
        state[1] (N) represents the % health of this enemy in increments of 10%
        """
        N = math.floor((unit.current_hp / unit.hp_max) * 10)
        if N == 10:  # State space for N is in the range [0, 10), so if it was 10 we'd go out of bounds, so clip it
            N = 9

        E = 0
        for enemy_unit in enemy_team:
            valid_moves = self.map.get_valid_move_coordinates(enemy_unit, enemy_team, ally_team)
            for move in valid_moves:
                x = move[0]
                y = move[1]
                attackable_units = feutils.get_attackable_units(enemy_unit, ally_team, x, y)
                if unit in attackable_units:
                    E += 1
                    break  # Each enemy unit counts for, at most, ONE increment of E

            if E == 15:
                break

        return E, N

    def generate_valid_moves(self, action, unit, ally_team, enemy_team):
        """
        Generates a list of valid move coordinates given an action. The unit will be able to do
        that action at every coordinate in the returned list

        :param action: The action the user is attempting to do. (0 for Wait, 1 for Item, 2 for Attack)
        :param unit: The unit we are checking
        :param ally_team: The allied team to unit (blue or red)
        :param enemy_team: The adversarial team to unit (blue or red)
        :return: A list of tuples representing x,y pairs. The unit will be able to execute the action passed in
        at every coordinate in the list.
        """
        all_valid_move_coordinates = self.map.get_valid_move_coordinates(unit, ally_team, enemy_team)

        if action == 0 or action == 1:  # The unit will be able to wait/use an item at every coordinate they can move to
            return all_valid_move_coordinates

        valid_move_actions = []
        for x, y in all_valid_move_coordinates:
            attackable = feutils.get_attackable_units(unit, enemy_team, x, y)
            if len(attackable) > 0:
                valid_move_actions.append((x,y))

        return valid_move_actions

    def generate_action_mask(self, unit, ally_team, enemy_team):
        """

        :param ally_team:
        :param unit:
        :param enemy_team:
        :return:
        """
        valid_coords = self.map.get_valid_move_coordinates(unit, ally_team, enemy_team)
        return self.map.get_all_valid_actions(unit, enemy_team, valid_coords)

    def execute_red_phase(self, blue_team, red_team):
        """
        Iterates through the red team and executes each action on the environment.

        :param blue_team: The blue team
        :param red_team: The red team
        :return: state, done, info\n
            state -> the state of blue_team[0] after the red_team has finished executing its turn
            done -> whether or not the episode is done after the red team took their turn
            info -> dictionary with information about the step:
                info['winner'] -> if done is True, this will hold the team that won (blue or red)
                info['method'] -> if done is True, this will hold how the winning team won
        """
        done = False
        info = {}

        for red_unit in red_team:
            action = red_unit.determine_action(None, self, red_team, blue_team)
            move = red_unit.determine_move(action, red_team, blue_team, self)
            _, _, done, info = self.step(red_unit, move, action, red_team, blue_team)

            if done:
                break

        self.turn_count += 1
        if self.turn_count >= self.turn_limit:
            done = True

        return self.obtain_state(blue_team[0], blue_team, red_team), done, info

    def step(self, unit, move, action, ally_team, enemy_team):
        """
        Steps the environment given the unit, move, and action to be executed by said unit

        :param ally_team: The team allied to unit (blue or red)
        :param enemy_team: The adversarial team to unit (blue or red)
        :param unit: The unit who will affect the environment in some way
        :param move: The coordinates the unit will move to (tuple as x,y)
        :param action: The action the unit will take (attack, wait, item)
        :return: next_state, reward, done, info
            next_state -> the unit's state given the action and move they just did
            reward -> The reward the environment gave the unit for taking said action
            done -> whether or not the episode is done after the action
            info -> dictionary with information about the step:
                        info['winner'] -> if done is True, this will hold the team that won (blue or red)
                        info['method'] -> if done is True, this will hold how the winning team won
        """
        done = False
        heal_total = None
        killed_enemy = False
        info = {}

        # Always move
        unit.goto(move[0], move[1])

        if action == 2:  # Attack
            target_unit = unit.determine_target(self, enemy_team)
            combat_stats = combat.get_combat_stats(unit, target_unit, self.map)
            result = combat.simulate_combat(combat_stats)

            if result is CombatResults.DEFENDER_DEATH:
                if target_unit.terminal_condition:
                    done = True
                else:
                    target_unit.close()
                    enemy_team.remove(target_unit)
                    killed_enemy = True

            elif result is CombatResults.ATTACKER_DEATH:
                if unit.terminal_condition:
                    done = True
                else:
                    unit.close()
                    ally_team.remove(unit)

        elif action == 1:  # Item
            item_index = unit.determine_item_to_use(self, enemy_team)
            heal_total = unit.use_item(item_index)

        # The other action is 0, but that is just wait, so don't do anything

        state = self.obtain_state(unit, ally_team, enemy_team)
        reward = self.reward(unit, action, killed_enemy, heal_total)

        return state, reward, done, info

    def reward(self, unit, action, killed_enemy, heal_total=None):
        if unit.current_hp <= 0:
            return -20.0

        if killed_enemy:
            return 10.0

        if action == 0:
            return 1.0  # Not dying is still technically good

        if action == 1:
            return 1.0  # temporary

        return 0.0  # temporary


    def reset(self):
        """
        Resets the environment to be ready for a new game

        :return:
        """
        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False
        self.map, self.number_map = self.map_factory.generate_map()

