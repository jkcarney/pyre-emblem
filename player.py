import random
from abc import ABC, abstractmethod
from map import Map, Tile
from item import Item


class Player(ABC):
    @abstractmethod
    def determine_move_coordinates(self, all_units, tile_map, this_unit):
        pass

    @abstractmethod
    def determine_action(self, all_units, tile_map, this_unit, x, y):
        pass


class RandomPlayer(Player):

    def determine_move_coordinates(self, all_units, tile_map, this_unit):
        valid_moves = tile_map.get_valid_move_coordinates(this_unit)
        return random.choice(valid_moves)

    def determine_action(self, all_units, tile_map, this_unit, x, y):
        potential_actions = tile_map.valid_actions_at_position(this_unit, all_units, x, y)
        return random.choice(potential_actions)
