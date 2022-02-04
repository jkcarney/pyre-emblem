import random
import numpy as np
from matplotlib import pyplot, colors
import copy

from numpy import arange

import feutils
from map import Map, Tile


class MapLayerFactory:
    def __init__(self, iterations, live_low, live_high, birth_low, birth_high):
        self.live_low, self.live_high = live_low, live_high
        self.birth_low, self.birth_high = birth_low, birth_high

        self.iterations = iterations

    def generate_binary_map(self, x, y):
        ground_grid = self.generate_ground(x, y)
        return ground_grid

    def generate_ground(self, x, y):
        grid = np.ndarray((x, y))
        self.populate_randomly(grid, x, y)

        for i in range(self.iterations):
            self.advance_generation(grid)

        return grid

    def populate_randomly(self, grid, x, y):
        for i in range(x):
            for j in range(y):
                grid[i, j] = bool(random.getrandbits(1))

    def advance_generation(self, grid):
        grid_clone = copy.deepcopy(grid)

        for i in range(len(grid_clone)):
            for j in range(len(grid_clone[0])):
                neighbors = self.count_alive_neighbors(grid_clone, i, j)
                # Birth
                if not grid_clone[i, j]:
                    if self.birth_low <= neighbors <= self.birth_high:
                        grid[i, j] = True
                # Death
                else:
                    if neighbors < self.live_low or neighbors > self.live_high:
                        grid[i, j] = False

    def count_alive_neighbors(self, grid, x, y):
        neighbors = 0
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i + x >= 0 and j + y >= 0:
                    if grid[i + x, j + y]:
                        neighbors += 1

        return neighbors


class OutdoorMapFactory:
    def __init__(self, x_min, x_max, y_min, y_max, ):
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

        self.grass_water_factory = MapLayerFactory(5, 2, 7, 3, 8)
        self.forest_factory = MapLayerFactory(5, 2, 6, 4, 7)
        self.mountain_factory = MapLayerFactory(2, 3, 8, 3, 8)

    def generate_map(self):
        x = random.randint(self.x_min, self.x_max)
        y = random.randint(self.y_min, self.y_max)

        grass_water_grid = self.grass_water_factory.generate_binary_map(x, y)
        forest_grid = self.forest_factory.generate_binary_map(x, y)
        mountain_grid = self.mountain_factory.generate_binary_map(x, y)

        final_map = np.ndarray((x, y), dtype='<U8')
        number_map = np.ndarray((x, y))

        for i in range(x):
            for j in range(y):
                #Alive represents lake, dead represents plains
                if grass_water_grid[i, j]:
                    final_map[i, j] = 'Lake'
                    number_map[i, j] = 1
                else:
                    final_map[i, j] = 'Plain'
                    number_map[i, j] = 0

                if final_map[i, j] == 'Plain' and forest_grid[i, j]:
                    final_map[i, j] = 'Forest'
                    number_map[i, j] = 2

                if final_map[i, j] != 'Lake' and mountain_grid[i, j]:
                    final_map[i, j] = 'Mountain'
                    number_map[i, j] = 3

        return Map(x, y, final_map), number_map


if __name__ == '__main__':
    factory = OutdoorMapFactory(7, 12, 7, 12)
    fe_map, number_map = factory.generate_map()
    print(fe_map)

    colormap = colors.ListedColormap(["green", "blue", "darkgreen", "brown"])

    pyplot.imshow(number_map,
                  cmap=colormap,
                  origin='lower',
                  interpolation='none')
    pyplot.show()