import random
from abc import ABC, abstractmethod
from map import Map, Tile
from item import Item


class Agent(ABC):
    @abstractmethod
    def determine_move_coordinates(self, friend_units, enemy_units, tile_map: Map, this_unit):
        pass

    @abstractmethod
    def determine_action(self, friend_units, enemy_units, tile_map: Map, this_unit):
        pass


class RandomAgent(Agent):
    def determine_move_coordinates(self, friend_units, enemy_units, tile_map: Map, this_unit):
        valid_moves = tile_map.get_valid_move_coordinates(this_unit, friend_units, enemy_units)
        return random.choice(valid_moves)

    def determine_action(self, friend_units, enemy_units, tile_map: Map, this_unit):
        all_move_coordinates = tile_map.get_valid_move_coordinates(this_unit, friend_units, enemy_units)
        potential_actions = tile_map.get_all_valid_actions(this_unit, enemy_units, all_move_coordinates)
        return random.choice(potential_actions)

