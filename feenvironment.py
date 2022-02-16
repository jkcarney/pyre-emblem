import gym
from gym import error, spaces, utils
from gym.utils import seeding

import map_factory
import map


class FireEmblemEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, blue_team: list, red_team: list):
        super(FireEmblemEnvironment, self).__init__()

        self.blue_team = blue_team
        self.red_team = red_team

        self.map_factory = map_factory.OutdoorMapFactory(15, 20, 15, 20)
        self.map, self.number_map = self.map_factory.generate_map()

        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

    def step(self, action):
        pass

    def reset(self):
        # Units?
        self.map, self.number_map = self.map_factory.generate_map()

        self.turn_count = 0
        self.blue_victory = False
        self.red_victory = False

        self.current_phase = 'Blue'
        self.current_unit = 0

    def render(self, mode="human"):
        pass

    def close(self):
        pass
