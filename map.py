import feutils
from action import Action


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

    def valid_actions_at_position(self, unit, all_units, x, y):
        """
        Assuming unit was at coordinates x and y, what are the valid actions they could take?

        This function does not verify that the unit, given their current position, movement stat, and movement class,
        could move to position x and y

        Units can always wait at a given space, while the usability of items is limited to if they have any left to
        use. Attacking is also limited to enemy units within any of their items attack range

        :param unit: The unit who's actions we are checking
        :param x: The theoretical x position of the unit
        :param y: The theoretical y position of the unit
        :return: A list of actions the unit can take. ('Wait', and/or 'Item', and/or 'Attack')
        """
        valid_actions = [Action('Wait', None)]

        all_consumables = unit.get_all_consumables()
        for consumable in all_consumables:
            valid_actions.append(Action('Item', consumable))

        attackable_units = self.get_attackable_units(unit, all_units, x, y)
        for u in attackable_units:
            valid_actions.append(Action('Attack', u))

        return valid_actions

    def get_attackable_units(self, unit, all_units: list, x = None, y = None):
        """
        Gets all attackable units within range of unit.

        x and y are optional parameters. If specified, it will check if unit could attack any units at the
        given x and y. Otherwise, it defaults to the unit's current x and y

        :param all_units: All the units currently in the game
        :param unit: The unit whos attack range we are checking
        :param x: optional x to check from
        :param y: optional y to check from
        :return:
        """
        attackable_units = []

        if x is None or y is None:
            x, y = unit.x, unit.y

        atk_range = unit.get_attack_range()
        for candidate in all_units:
            # Checks to see if the candidate and unit are on opposing teams
            if candidate.ally != unit.ally:
                distance = self.manhattan_distance(x, y, candidate.x, candidate.y)
                if distance in atk_range:
                    attackable_units.append(candidate)

        return attackable_units

    def get_valid_move_coordinates(self, unit, ally_units, enemy_units):
        """
        Retrieves all the tiles the unit could move to given their current position, movement stat, and movement class,
        as a set of tuples representing x y pairs

        :param unit: The unit who we are checking
        :return: A set of tuples that represent x y pairs
        """
        movement = unit.move
        terrain_group = unit.terrain_group

        # The tile the unit is standing on is always assumed to be a valid move tile.
        valid_tiles = {(unit.x, unit.y)}

        self.__calculate_tile__(unit.x + 1, unit.y, movement, terrain_group, 0, valid_tiles, enemy_units)
        self.__calculate_tile__(unit.x - 1, unit.y, movement, terrain_group, 0, valid_tiles, enemy_units)
        self.__calculate_tile__(unit.x, unit.y + 1, movement, terrain_group, 0, valid_tiles, enemy_units)
        self.__calculate_tile__(unit.x, unit.y - 1, movement, terrain_group, 0, valid_tiles, enemy_units)

        for u in ally_units + enemy_units:
            if u is not unit:
                position = u.x,u.y
                if position in valid_tiles:
                    valid_tiles.remove(position)

        return valid_tiles

    def __calculate_tile__(self, x, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units):
        for enemy in enemy_units:
            if (enemy.x,enemy.y) == (x,y):
                return

        accumulated_cost += self.grid[x][y].get_unit_cost(terrain_group)

        if accumulated_cost > movement:
            return

        if x < 0 or x >= self.x:
            return

        if y < 0 or y >= self.y:
            return

        valid_tiles.add((x, y))

        self.__calculate_tile__(x + 1, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x - 1, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x, y + 1, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x, y - 1, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
