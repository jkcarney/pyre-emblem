import feutils
import PIL
from PIL import Image


class Map:
    def __init__(self, map_number):
        self.x, self.y = self.__load_map_size__(map_number)

    def __load_map_size__(self, number):
        path = f'map_images/{number}.png'
        image = PIL.Image.open(path)
        return int(image.size[0]/16), int(image.size[1]/16)


class Tile:
    def __init__(self, tile_name):
        pass
