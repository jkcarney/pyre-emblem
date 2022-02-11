import random
from abc import ABC, abstractmethod
from map import Map, Tile
from item import Item


class Player(ABC):
    @abstractmethod
    def determine_move_coordinates(self, friend_units, enemy_units, tile_map: Map, this_unit):
        pass

    @abstractmethod
    def determine_action(self, enemy_units, tile_map: Map, this_unit, x, y):
        pass


class RandomPlayer(Player):
    def determine_move_coordinates(self, friend_units, enemy_units, tile_map: Map, this_unit):
        valid_moves = tile_map.get_valid_move_coordinates(this_unit, friend_units, enemy_units)
        return random.choice(valid_moves)

    def determine_action(self, enemy_units, tile_map: Map, this_unit, x, y):
        potential_actions = tile_map.valid_actions_at_position(this_unit, enemy_units, x, y)
        return random.choice(potential_actions)

