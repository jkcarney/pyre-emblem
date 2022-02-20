import combat
from unit import *
from combat import *
from map import Map
from item import Item
from agent import Agent, RandomAgent
from map_factory import OutdoorMapFactory
import unit_populator

# Games will go up to not including TURN_LIMIT turns
# (A turn is defined as one side moving all their units)
TURN_LIMIT = 101


class FireEmblem:
    def __init__(self, tile_map: Map, blue_team: list, red_team: list, blue_player: Agent, red_player: Agent):
        self.map = tile_map
        self.blue_team = blue_team
        self.red_team = red_team
        self.blue_player = blue_player
        self.red_player = red_player

        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False

        # Current unit is an index to the unit lists, not a unit object.
        self.current_unit = 0
        self.current_phase = 'Blue'

    def step(self):
        if self.current_phase == 'Blue':
            self.__blue_phase()
            self.current_unit += 1

            if self.current_unit >= len(self.blue_team):
                print('-- RED PHASE --')
                self.current_phase = 'Red'
                self.current_unit = 0

        elif self.current_phase == 'Red':
            self.__red_phase()
            self.current_unit += 1

            if self.current_unit >= len(self.red_team):
                self.current_phase = 'Blue'
                self.current_unit = 0
                self.turn_count += 1
                print('-- BLUE PHASE --')
                print(f'-- TURN {self.turn_count} --')

        if self.turn_count == TURN_LIMIT:
            self.red_victory = True

        if self.blue_victory:
            return 1
        if self.red_victory:
            return -1

        return 0

    def __blue_phase(self):
        unit = self.blue_team[self.current_unit]
        action_choice = self.blue_player.determine_action(self.blue_team, self.red_team, self.map, unit)
        x, y = action_choice.x, action_choice.y
        unit.goto(x, y)
        print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")

        if action_choice.is_attack():
            # Defender in this case is from self.enemies
            defender = action_choice.action_item
            combat_stats = combat.get_combat_stats(unit, defender, self.map)
            result = combat.simulate_combat(combat_stats)
            print(f"\t {result.name}")

            if result is CombatResults.DEFENDER_DEATH:
                self.red_team.remove(defender)
                if not self.red_team:
                    self.blue_victory = True

            elif result is CombatResults.ATTACKER_DEATH:
                if unit.terminal_condition:
                    self.red_victory = True
                self.blue_team.remove(unit)

        elif action_choice.is_item():
            item_to_use = action_choice.action_item
            heal_amount = item_to_use.info['heal_amount']
            unit.heal(heal_amount)
            item_to_use.info['uses'] -= 1
            if item_to_use.info['uses'] == 0:
                unit.inventory.remove(item_to_use)

    def __red_phase(self):
        unit = self.red_team[self.current_unit]
        action_choice = self.red_player.determine_action(self.red_team, self.blue_team, self.map, unit)
        x, y = action_choice.x, action_choice.y
        unit.goto(x, y)
        print(f"{unit.name} moved to coordinates {unit.x}, {unit.y} and chose {action_choice.name}")

        if action_choice.is_attack():
            # Defender in this case is from self.enemies
            defender = action_choice.action_item
            combat_stats = combat.get_combat_stats(unit, defender, self.map)
            result = combat.simulate_combat(combat_stats)
            print(f"\t {result.name}")

            if result is CombatResults.DEFENDER_DEATH:
                if unit.terminal_condition:
                    self.red_victory = True
                self.blue_team.remove(defender)

            elif result is CombatResults.ATTACKER_DEATH:
                self.red_team.remove(unit)
                if not self.red_team:
                    self.blue_victory = True

        elif action_choice.is_item():
            item_to_use = action_choice.action_item
            heal_amount = item_to_use.info['heal_amount']
            unit.heal(heal_amount)
            item_to_use.info['uses'] -= 1
            if item_to_use.info['uses'] == 0:
                unit.inventory.remove(item_to_use)


if __name__ == "__main__":
    map_factory = OutdoorMapFactory(15, 15, 15, 15)
    tile_map,number_tile_map = map_factory.generate_map()

    print(tile_map)

    blue_team = unit_populator.generate_blue_team(tile_map)
    red_team = unit_populator.generate_red_team(tile_map, blue_team)

    result = 0

    game = FireEmblem(tile_map, blue_team, red_team, RandomAgent(), RandomAgent())
    while result == 0:
        result = game.step()

    print(f"Here's the result of the game: {result}")
