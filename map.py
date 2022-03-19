import random
import numpy as np
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

    def get_all_valid_actions(self, unit, enemy_units, all_move_coordinates):
        """
        Assuming unit was at coordinates x and y, what are the valid actions they could take?

        This function does not verify that the unit, given their current position, movement stat, and movement class,
        could move to position x and y

        Units can always wait at a given space, while the usability of items is limited to if they have any left to
        use. Attacking is also limited to enemy units within any of their items attack range

        :param enemy_units: The units who we will check to see if we can attack
        :param unit: The unit who's actions we are checking
        :param all_move_coordinates: all the move coordinates the unit can move to
        :return: An action mask; a boolean array of size 3. False means the unit CAN take the action. True means the
        unit CANNOT take the action, and will be masked ultimately.
        """
        valid_actions = np.array([False, True, True])

        if unit.has_consumable():
            valid_actions[1] = False

        for x, y in all_move_coordinates:
            attackable_units = self.get_attackable_units(unit, enemy_units, x, y)
            if len(attackable_units) != 0:
                valid_actions[2] = False

        return valid_actions

    def get_attackable_units(self, unit, enemy_units: list, x=None, y=None):
        """
        Gets all attackable units within range of unit.

        x and y are optional parameters. If specified, it will check if unit could attack any units at the
        given x and y. Otherwise, it defaults to the unit's current x and y

        :param enemy_units: All the units currently in the game
        :param unit: The unit whos attack range we are checking
        :param x: optional x to check from
        :param y: optional y to check from
        :return:
        """
        attackable_units = []

        if x is None or y is None:
            x, y = unit.x, unit.y

        atk_range = unit.get_attack_range()
        for candidate in enemy_units:
            # Checks to see if the candidate and unit are on opposing teams
            distance = self.manhattan_distance(x, y, candidate.x, candidate.y)
            if distance in atk_range:
                attackable_units.append(candidate)

        return attackable_units

    def get_valid_move_coordinates(self, unit, ally_units, enemy_units):
        """
        Retrieves all the tiles the unit could move to given their current position, movement stat, and movement class,
        as a set of tuples representing x y pairs

        :param enemy_units: list of Units that the unit is fighting (opposite team)
        :param ally_units: list of Units that the unit is allied with (same team)
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
                position = u.x, u.y
                if position in valid_tiles:
                    valid_tiles.remove(position)

        return list(valid_tiles)

    def __calculate_tile__(self, x, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units):
        if x < 0 or x >= self.x:
            return

        if y < 0 or y >= self.y:
            return

        for enemy in enemy_units:
            if (enemy.x, enemy.y) == (x, y):
                return

        accumulated_cost += self.grid[x][y].get_unit_cost(terrain_group)

        if accumulated_cost > movement:
            return

        valid_tiles.add((x, y))

        self.__calculate_tile__(x + 1, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x - 1, y, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x, y + 1, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)
        self.__calculate_tile__(x, y - 1, movement, terrain_group, accumulated_cost, valid_tiles, enemy_units)

    def set_red_unit_start_coordinates(self, red_unit, red_team, blue_team):
        candidate_coordinates = []
        terrain_group = red_unit.terrain_group
        for i in range(self.x):
            for j in range(self.y):
                terrain_cost = self.grid[i][j].get_unit_cost(terrain_group)
                if terrain_cost != 999:
                    candidate_coordinates.append((i, j))

        for unit in red_team:
            coords = (unit.x, unit.y)
            if coords in candidate_coordinates:
                candidate_coordinates.remove(coords)

        for unit in blue_team:
            coords = (unit.x, unit.y)
            if coords in candidate_coordinates:
                candidate_coordinates.remove(coords)

        chosen_coord = random.choice(candidate_coordinates)
        red_unit.goto(chosen_coord[0], chosen_coord[1])

    def __get_valid_corners(self):
        all_corners = [
            (0, 0),
            (0, self.y - 1),
            (self.x - 1, self.y - 1),
            (self.x - 1, 0)
        ]

        valid_corners = []

        for coordinates in all_corners:
            terrain_cost = self.grid[coordinates[0]][coordinates[1]].get_unit_cost("Foot")
            if terrain_cost != 999:
                valid_corners.append(coordinates)

        return valid_corners

    def __get_N_closest_tiles(self, starting_point, n):
        closest = set()
        x, y = starting_point

        self.__recurse_on_tiles(x + 1, y, closest, n, 0)
        self.__recurse_on_tiles(x - 1, y, closest, n, 0)
        self.__recurse_on_tiles(x, y + 1, closest, n, 0)
        self.__recurse_on_tiles(x, y - 1, closest, n, 0)

        return list(closest)

    def __recurse_on_tiles(self, x, y, closest_tiles, n, length):
        if x < 0 or x >= self.x:
            return

        if y < 0 or y >= self.y:
            return

        if length >= n:
            return

        # Limit valid starting coordinates to standable tiles for any unit, aka foot units
        cost = self.grid[x][y].get_unit_cost("Foot")
        if cost == 999:
            return

        closest_tiles.add((x, y))
        length += 1

        self.__recurse_on_tiles(x + 1, y, closest_tiles, n, length)
        self.__recurse_on_tiles(x - 1, y, closest_tiles, n, length)
        self.__recurse_on_tiles(x, y + 1, closest_tiles, n, length)
        self.__recurse_on_tiles(x, y - 1, closest_tiles, n, length)

    def set_all_blue_start_coordinates(self, terminal_unit, blue_team):
        starting_point = random.choice(self.__get_valid_corners())
        print(f'---{starting_point[0]}, {starting_point[1]}---')
        terminal_unit.goto(starting_point[0], starting_point[1])
        starting_coordinates = self.__get_N_closest_tiles(starting_point, len(blue_team) + 2)

        for unit in blue_team:
            starting_x, starting_y = random.choice(starting_coordinates)
            unit.goto(starting_x, starting_y)
            starting_coordinates.remove((starting_x, starting_y))
