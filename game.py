import unit
import combat
from map import Map
import item

class FireEmblem:
    def __init__(self, tile_map: Map, blue_team: list, red_team: list, blue_controller, red_controller):
        self.map = tile_map
        self.allies = blue_team
        self.enemies = red_team
        self.ally_controller = blue_controller
        self.enemy_controller = red_controller
