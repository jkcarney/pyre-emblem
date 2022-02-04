import feutils

def get_random_tile_name():
    return ''


class Map:
    def __init__(self, x_tiles, y_tiles, matrix_tile_names):
        self.x, self.y = x_tiles, y_tiles
        self.grid = [[0 for i in range(y_tiles)] for j in range(x_tiles)]

        for i in range(x_tiles):
            for j in range(y_tiles):
                self.grid[i][j] = Tile(matrix_tile_names[i, j])

    def __str__(self):
        result = ''
        for i in range(self.x):
            for j in range(self.y):
                result += str(self.grid[i][j]) + ' '
            result += '\n'
        return result


class Tile:
    def __init__(self, tile_name):
        self.name = tile_name
        tile_data = feutils.tile_info_lookup(tile_name)
        self.avoid = tile_data['avoid']
        self.defense = tile_data['def']
        del tile_data['avoid']
        del tile_data['def']

        self.movement_costs = tile_data

    def __str__(self):
        return self.name



