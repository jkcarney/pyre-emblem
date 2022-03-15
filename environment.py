import map_factory
import unit_populator


class Environment:
    def __init__(self):
        self.map_factory = map_factory.OutdoorMapFactory(15, 18, 15, 18)
        self.map, self.number_map = self.map_factory.generate_map()

        self.blue_team = unit_populator.generate_blue_team(self.map)
        self.red_team = unit_populator.generate_red_team(self.map, self.blue_team)

        self.turn_count = 0
        self.turn_limit = 100
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
