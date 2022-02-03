import random
import numpy as np
from matplotlib import pyplot, colors
import copy
import feutils
from map import Map, Tile, get_random_tile_name


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
        self.mountain_factory = MapLayerFactory(5, 1, 8, 4, 8)

    def generate_map(self):
        x = random.randint(self.x_min, self.x_max)
        y = random.randint(self.y_min, self.y_max)

        grass_water_grid = self.grass_water_factory.generate_binary_map(x, y)
        forest_grid = self.forest_factory.generate_binary_map(x, y)
        mountain_grid = self.mountain_factory.generate_binary_map(x, y)

        return mountain_grid


factory = OutdoorMapFactory(7, 12, 7, 12)
outer_grid = factory.generate_map()
print(outer_grid)
colormap = colors.ListedColormap(["green", "blue"])
pyplot.figure(figsize=(5,5))
pyplot.imshow(outer_grid, cmap=colormap)
pyplot.show()

