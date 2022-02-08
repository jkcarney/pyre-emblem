import unit
import combat
from map import Map
import item
from player import Player


class FireEmblem:
    def __init__(self, tile_map: Map, blue_team: list, red_team: list, blue_player: Player, red_player: Player):
        self.map = tile_map
        self.allies = blue_team
        self.enemies = red_team
        self.ally_player = blue_player
        self.enemy_player = red_player

    

