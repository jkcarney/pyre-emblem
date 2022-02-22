import random
from abc import ABC, abstractmethod
import numpy as np

from fe_env.envs import FireEmblemEnvironment
from map import Map, Tile
from item import Item
import gym
import feutils


class Agent(ABC):
    @abstractmethod
    def determine_action(self, env: FireEmblemEnvironment):
        pass

    def action_is_valid(self, action, valid_actions):
        return np.any(np.all(action == valid_actions, axis=1))


class RandomAgent(Agent):
    def determine_action(self, env: FireEmblemEnvironment):
        valid = False
        random_action = env.action_space.sample()
        all_valid_actions = env.unwrapped.get_valid_actions_in_state()

        while not valid:
            if self.action_is_valid(random_action, all_valid_actions):
                valid = True
            else:
                random_action = env.action_space.sample()

        return random_action


class DumbRedAgent(Agent):
    def determine_action(self, env: FireEmblemEnvironment):
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

