import gym
from gym import error, spaces, utils
from gym.utils import seeding

import map_factory
import map
from action import Action
import combat
from combat import CombatResults, CombatSummary


class FireEmblemEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, blue_team: list, red_team: list):
        super(FireEmblemEnvironment, self).__init__()

        self.blue_team = blue_team
        self.red_team = red_team

        self.map_factory = map_factory.OutdoorMapFactory(15, 20, 15, 20)
        self.map, self.number_map = self.map_factory.generate_map()

        self.turn_count = 0
        self.turn_limit = 100
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

    def step(self, action):
        if self.current_phase == 'Blue':
            self.__blue_phase(action)
            self.current_unit += 1

            if self.current_unit >= len(self.blue_team):
                self.current_phase = 'Red'
                self.current_unit = 0

        elif self.current_phase == 'Red':
            self.__red_phase(action)
            self.current_unit += 1

            if self.current_unit >= len(self.red_team):
                self.current_phase = 'Blue'
                self.current_unit = 0
                self.turn_count += 1

        if self.turn_count == self.turn_limit:
            self.red_victory = True

        done = False
        reward = -self.turn_count

        # return observation, reward, done, info
        if self.red_victory:
            done = True
            reward = -100

        if self.blue_victory:
            done = True
            reward = 100

        return None, reward, done, {}

    def __blue_phase(self, action_choice):
        unit = self.blue_team[self.current_unit]
        x, y = action_choice.x, action_choice.y
        unit.goto(x, y)

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

        if action_choice.is_attack():
            # Defender in this case is from self.enemies
            defender = action_choice.action_item
            combat_stats = combat.get_combat_stats(unit, defender, self.map)
            result = combat.simulate_combat(combat_stats)
            print(f"\t {result.name}")

            if result is CombatResults.DEFENDER_DEATH:
                if unit.terminal_condition:
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
        # Units?
        self.map, self.number_map = self.map_factory.generate_map()

        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

    def render(self, mode="human"):
        pass

    def close(self):
        pass
