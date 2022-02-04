import feutils


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

    def get_tile(self, x, y) -> Tile:
        return self.grid[x][y]

    def get_tile_movement_costs(self, x, y):
        return self.grid[x][y].movement_costs
