import combat
from unit import *
from combat import *
from map import Map
from item import Item
from player import Player, RandomPlayer
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
            print(f"Turn: {self.turn_count}")
            # Ally unit phase
            for unit in self.allies:
                new_coords = self.ally_controller.determine_move_coordinates(self.allies, self.enemies, self.map, unit)
                unit.goto(new_coords[0], new_coords[1])
                action_choice = self.ally_controller.determine_action(self.enemies, self.map, unit, unit.x, unit.y)
                print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")
                if action_choice.is_attack():
                    # Defender in this case is from self.enemies
                    defender = action_choice.action_item
                    combat_stats = combat.get_combat_stats(unit, defender, self.map)
                    result = combat.simulate_combat(combat_stats)
                    print(f"\t {result.name}")

                    if result is CombatResults.DEFENDER_DEATH:
                        self.enemies.remove(defender)
                        if not self.enemies:
                            self.win_condition_encountered = True

                    elif result is CombatResults.ATTACKER_DEATH:
                        if unit.terminal_condition:
                            self.loss_condition_encountered = True
                        self.allies.remove(unit)

                elif action_choice.is_item():
                    item_to_use = action_choice.action_item
                    heal_amount = item_to_use.info['heal_amount']
                    unit.heal(heal_amount)
                    item_to_use.info['uses'] -= 1
                    if item_to_use.info['uses'] == 0:
                        unit.inventory.remove(item_to_use)

                if self.win_condition_encountered:
                    return 1
                elif self.loss_condition_encountered:
                    return -1

            # Enemy movement phase
            for unit in self.enemies:
                new_coords = self.enemy_controller.determine_move_coordinates(self.enemies, self.allies, self.map, unit)
                unit.goto(new_coords[0], new_coords[1])
                action_choice = self.enemy_controller.determine_action(self.allies, self.map, unit, unit.x, unit.y)
                print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")
                if action_choice.is_attack():
                    # Defender in this case is from self.allies
                    defender = action_choice.action_item
                    combat_stats = combat.get_combat_stats(unit, defender, self.map)
                    result = combat.simulate_combat(combat_stats)
                    print(f"\t {result.name}")

                    if result is CombatResults.DEFENDER_DEATH:
                        if defender.terminal_condition:
                            self.loss_condition_encountered = True
                        self.allies.remove(defender)

                    elif result is CombatResults.ATTACKER_DEATH:
                        self.enemies.remove(unit)
                        if not self.enemies:
                            self.win_condition_encountered = True

                elif action_choice.is_item():
                    item_to_use = action_choice.action_item
                    heal_amount = item_to_use.info['heal_amount']
                    unit.heal(heal_amount)
                    item_to_use.info['uses'] -= 1
                    if item_to_use.info['uses'] == 0:
                        unit.inventory.remove(item_to_use)

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


if __name__ == "__main__":
    map_factory = OutdoorMapFactory(10, 15, 10, 15)
    tile_map = map_factory.generate_map()[0]

    lyn = Unit(0xceb4, 0, 0, 2, 0x0204, 17, 6, 8, 10, 6, 2, 0, 0, True, [0x1, 0x6b], True)
    bandit = Unit(0xe9b8, 0, 1, 2, 0x1410, 21, 4, 1, 4, 0, 3, 0, 0, False, [0x1f], False)

    allies = [lyn]
    enemies = [bandit]

    game = FireEmblem(tile_map, allies, enemies, RandomPlayer(), RandomPlayer())
    result = game.run()

    print(f"Here's the result of the game: {result}")