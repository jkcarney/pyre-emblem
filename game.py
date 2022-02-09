import combat
from unit import *
from combat import *
from map import Map
from item import Item
from player import Player
from map_factory import OutdoorMapFactory


class FireEmblem:
    def __init__(self, tile_map: Map, blue_team: list, red_team: list, blue_player: Player, red_player: Player):
        self.map = tile_map
        self.allies = blue_team
        self.enemies = red_team
        self.ally_player = blue_player
        self.enemy_player = red_player
        self.turn_count = 0

        self.loss_condition_encountered = False
        self.win_condition_encountered = False

    def check_for_win_condition(self):
        if self.enemies is []:
            self.win_condition_encountered = True
            return True

    def check_for_loss_condition(self):
        if self.turn_count == 200:
            self.loss_condition_encountered = True
            return True

    def run(self):
        while not self.loss_condition_encountered and not self.win_condition_encountered:
            self.turn_count += 1

            for unit in self.allies:
                new_coords = self.ally_player.determine_move_coordinates(self.allies + self.enemies, self.map, unit)
                unit.goto(new_coords[0], new_coords[1])
                action_choice = self.ally_player.determine_action(self.allies + self.enemies, self.map, unit, unit.x, unit.y)

                if action_choice.is_attack():
                    enemy = action_choice.action_item
                    combat_stats = combat.get_combat_stats(unit, enemy, self.map)
                    combat.simulate_combat(combat_stats)
                elif action_choice.is_item():
                    item_to_use = action_choice.action_item
                    heal_amount = item_to_use.info['heal_amount']
                    # do stuff lol

            # check for win/loss condition and break if so
            # enemy combat

            # check for win/loss condition



        if self.loss_condition_encountered:
            return -1
        else:
            return 1

