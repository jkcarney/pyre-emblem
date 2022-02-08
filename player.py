from abc import ABC, abstractmethod
from map import Map, Tile
from item import Item


class Player(ABC):
    @abstractmethod
    def move_unit(self, tile_map, unit):
        pass

    @abstractmethod
    def determine_action(self, tile_map, unit):
        pass

