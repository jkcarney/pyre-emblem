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

    def get_unit_cost(self, terrain_group):
        return self.movement_costs[terrain_group]

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

    def manhattan_distance(self, x1, y1, x2, y2):
        if x1 >= self.x or x2 >= self.x:
            raise IndexError('Tried to access indices out of map bounds (x coord)')
        if y1 >= self.y or y2 >= self.y:
            raise IndexError('Tried to access indices out of map bounds (y coord)')

        return abs(x1 - x2) + abs(y1 - y2)

    def get_valid_move_coordinates(self, unit):
        movement = unit.move
        terrain_group = unit.terrain_group
        valid_tiles = {(unit.x, unit.y)}

        self.__calculate_tile__(unit.x + 1, unit.y, movement, terrain_group, 0, valid_tiles)
        self.__calculate_tile__(unit.x - 1, unit.y, movement, terrain_group, 0, valid_tiles)
        self.__calculate_tile__(unit.x, unit.y + 1, movement, terrain_group, 0, valid_tiles)
        self.__calculate_tile__(unit.x, unit.y - 1, movement, terrain_group, 0, valid_tiles)

        return valid_tiles

    def __calculate_tile__(self, x, y, movement, terrain_group, accumulated_cost, valid_tiles):
        accumulated_cost += self.grid[x][y].get_unit_cost(terrain_group)

        if accumulated_cost > movement:
            return

        if x < 0 or x >= self.x:
            return

        if y < 0 or y >= self.y:
            return

        print(f'ADDING COORDINATES: {x} , {y}')
        print(f'\tACCUMULATED COST: {accumulated_cost}')

        valid_tiles.add((x, y))

        self.__calculate_tile__(x + 1, y, movement, terrain_group, accumulated_cost, valid_tiles)
        self.__calculate_tile__(x - 1, y, movement, terrain_group, accumulated_cost, valid_tiles)
        self.__calculate_tile__(x, y + 1, movement, terrain_group, accumulated_cost, valid_tiles)
        self.__calculate_tile__(x, y - 1, movement, terrain_group, accumulated_cost, valid_tiles)
