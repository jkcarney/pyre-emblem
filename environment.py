import map_factory
import unit_populator
from unit import Unit, BlueUnit, RedUnit
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

        self.current_phase = 'Blue'

    def obtain_state(self, unit, ally_team, enemy_team):
        """
        Obtains the state of the given unit, given the blue and red team

        :param unit: The unit whose state we will check
        :param ally_team: The blue team
        :param enemy_team: The red team
        :return: state -> a tuple that represents the state (ie, 5,6)
        state[0] represents the number of enemies that can attack this unit if they wanted to
        state[1] represents the % health of this enemy in increments of 10%
        """
        return 0, 0

    def generate_valid_moves(self, unit, blue_team, red_team):
        """

        :param unit:
        :param blue_team:
        :param red_team:
        :return:
        """
        pass

    def generate_action_mask(self, unit, ally_team, enemy_team):
        """

        :param ally_team:
        :param unit:
        :param enemy_team:
        :return:
        """
        return np.array([True, True, True])

    def execute_red_phase(self, blue_team, red_team):
        """
        Iterates through the red team and executes each action on the environment.

        :param blue_team: The blue team
        :param red_team: The red team
        :return: state, done
            state -> the state of blue_team[0] after the red_team has finished executing its turn
            done -> whether or not the episode is done after the red team took their turn
        """
        done = False
        for red_unit in red_team:
            action = red_unit.determine_action(self, blue_team, red_team)
            move = red_unit.determine_move(action, blue_team, red_team, self)
            _, _, done = self.step(red_unit, move, action, red_team, blue_team)

            if done:
                break

        return self.obtain_state(blue_team[0], blue_team, red_team), done

    def step(self, unit, move, action, ally_team, enemy_team):
        """
        Steps the environment given the unit and the move and action to be executed by said unit

        :param ally_team: The team allied to unit (blue or red)
        :param enemy_team: The adversarial team to unit (blue or red)
        :param unit: The unit who will affect the environment in some way
        :param move: The coordinates the unit will move to (tuple as x,y)
        :param action: The action the unit will take (attack, wait, item)
        :return: next_state, reward, done
            next_state -> the unit's state given the action and move they just did
            reward -> The reward the environment gave the unit for taking said action
            done -> whether or not the episode is done after the action
        """
        done = False
        heal_total = None

        # Always move
        unit.goto(move[0], move[1])

        if action == 'Attack':
            target_unit = unit.determine_target(self, enemy_team)
            combat_stats = combat.get_combat_stats(unit, target_unit, self.map)
            result = combat.simulate_combat(combat_stats)

            if result is CombatResults.DEFENDER_DEATH:
                if target_unit.terminal_condition:
                    done = True
                else:
                    enemy_team.remove(target_unit)

            elif result is CombatResults.ATTACKER_DEATH:
                if unit.terminal_condition:
                    done = True
                else:
                    ally_team.remove(unit)

        elif action == 'Item':
            item_index = unit.determine_item_to_use(self, enemy_team)
            heal_total = unit.use_item(item_index)

        state = self.obtain_state(unit, ally_team, enemy_team)
        reward = self.reward(unit, action, heal_total)

        return state, reward, done

    def reward(self, unit, action, heal_total=None):
        return 0.0

    def reset(self):
        """
        Resets the environment to be ready for a new game

        :return:
        """
        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False
        self.current_phase = 'Blue'
        self.map, self.number_map = self.map_factory.generate_map()
