import feutils
import numpy as np
import PIL
from PIL import Image


def get_random_tile_name():
    return ''


class Map:
    def __init__(self, x_tiles, y_tiles, matrix_tile_names):
        self.x, self.y = x_tiles, y_tiles
        self.grid = np.ndarray((self.x, self.y))
        for i in range(x_tiles):
            for j in range(y_tiles):
                self.grid[i, j] = Tile(matrix_tile_names[i, j])


    #def __load_map_size__(self, number):
    #    path = f'map_images/{number}.png'
    #    image = PIL.Image.open(path)
    #    # Each tile is 16x16, dividing the map sprite dimensions by that will give how many tiles there are
    #    return int(image.size[0]/16), int(image.size[1]/16)


class Tile:
    def __init__(self, tile_name):
        self.name = tile_name
        tile_data = feutils.tile_info_lookup(tile_name)
        self.avoid = tile_data['avoid']
        self.defense = tile_data['def']
        del tile_data['avoid']
        del tile_data['def']

        self.movement_costs = tile_data



