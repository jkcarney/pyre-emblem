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
        self.ally_controller = blue_player
        self.enemy_controller = red_player
        self.turn_count = 0

        self.loss_condition_encountered = False
        self.win_condition_encountered = False

    def run(self):
        while not self.loss_condition_encountered and not self.win_condition_encountered:
            self.turn_count += 1

            for unit in self.allies:
                new_coords = self.ally_controller.determine_move_coordinates(self.allies, self.enemies, self.map, unit)
                unit.goto(new_coords[0], new_coords[1])
                action_choice = self.ally_controller.determine_action(self.enemies, self.map, unit, unit.x, unit.y)

                if action_choice.is_attack():
                    enemy = action_choice.action_item
                    combat_stats = combat.get_combat_stats(unit, enemy, self.map)
                    result = combat.simulate_combat(combat_stats)

                    if result.DEFENDER_DEATH:
                        del enemy
                        if self.enemies is []:
                            self.win_condition_encountered = True

                    elif result.ATTACKER_DEATH:
                        if unit.terminal_condition:
                            self.loss_condition_encountered = True

                elif action_choice.is_item():
                    item_to_use = action_choice.action_item
                    heal_amount = item_to_use.info['heal_amount']
                    unit.heal(heal_amount)
                    item_to_use.info['uses'] -= 1

                    if item_to_use.info['uses'] == 0:
                        del item_to_use

                if self.win_condition_encountered:
                    return 1
                elif self.loss_condition_encountered:
                    return -1

            for unit in self.enemies:
                new_coords = self.enemy_controller.determine_move_coordinates(self.enemies, self.allies, self.map, unit)
                unit.goto(new_coords[0], new_coords[1])
                action_choice = self.enemy_controller.determine_action(self.allies, self.map, unit, unit.x, unit.y)

                if action_choice.is_attack():
                    enemy = action_choice.action_item
                    combat_stats = combat.get_combat_stats(unit, enemy, self.map)
                    result = combat.simulate_combat(combat_stats)

                    if result.DEFENDER_DEATH:
                        if unit.terminal_condition:
                            self.loss_condition_encountered = True

                    elif result.ATTACKER_DEATH:
                        del enemy
                        if self.enemies is []:
                            self.win_condition_encountered = True

                elif action_choice.is_item():
                    item_to_use = action_choice.action_item
                    heal_amount = item_to_use.info['heal_amount']
                    unit.heal(heal_amount)
                    item_to_use.info['uses'] -= 1

                    if item_to_use.info['uses'] == 0:
                        del item_to_use

                if self.win_condition_encountered:
                    return 1
                elif self.loss_condition_encountered:
                    return -1

            if self.turn_count == 100:
                self.loss_condition_encountered = True

            if self.win_condition_encountered:
                return 1
            elif self.loss_condition_encountered:
                return -1
