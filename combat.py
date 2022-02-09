import feutils
import item
import enum
import random
from unit import Unit
from item import Item
from item_type import *
from map import Map


class CombatResults(Enum):
    ATTACKER_DEATH = 0
    DEFENDER_DEATH = 1
    NO_DEATH = 2


class Combat:
    def __init__(self, hit_percent: float, might: int, crit_chance: float, doubling: bool):
        self.hit_chance = hit_percent
        self.might = might
        self.crit_chance = crit_chance
        self.doubling = doubling


class CombatSummary:
    def __init__(self, attacker: Unit, defender: Unit, attacker_summary: Combat, defender_summary: Combat):
        self.attacker = attacker
        self.defender = defender
        self.attacker_summary = attacker_summary
        self.defender_summary = defender_summary


def magic_triangle_bonus(attacker_tome: Item, defender_tome: Item):
    attk_enum = TomeType(attacker_tome.info['enum_type'])
    def_enum = TomeType(defender_tome.info['enum_type'])

    if attk_enum == TomeType.ANIMA:
        if def_enum == TomeType.LIGHT:
            return 1, 0.15
        elif def_enum == TomeType.DARK:
            return -1, -0.15
        else:
            return 0, 0.0

    if attk_enum == TomeType.LIGHT:
        if def_enum == TomeType.DARK:
            return 1, 0.15
        elif def_enum == TomeType.ANIMA:
            return -1, -0.15
        else:
            return 0, 0.0

    if attk_enum == TomeType.DARK:
        if def_enum == TomeType.ANIMA:
            return 1, 0.15
        elif def_enum == TomeType.LIGHT:
            return -1, -0.15
        else:
            return 0, 0.0

    return 0, 0.0


def weapon_triangle_bonus(attacker_item: Item, defender_item: Item):
    attk_enum = WeaponType(attacker_item.info['enum_type'])
    def_enum = WeaponType(defender_item.info['enum_type'])

    if attk_enum == WeaponType.SWORD:
        if def_enum == WeaponType.AXE:
            return 1, 0.15
        elif def_enum == WeaponType.LANCE:
            return -1, -0.15
        else:
            return 0, 0.0

    if attk_enum == WeaponType.LANCE:
        if def_enum == WeaponType.SWORD:
            return 1, 0.15
        elif def_enum == WeaponType.AXE:
            return -1, -0.15
        else:
            return 0, 0.0

    if attk_enum == WeaponType.AXE:
        if def_enum == WeaponType.LANCE:
            return 1, 0.15
        elif def_enum == WeaponType.SWORD:
            return -1, -0.15
        else:
            return 0, 0.0

    return 0, 0.0


def calculate_triangle_bonus(attacker: Unit, defender: Unit):
    """
    Gets a tuple representing the weapon triangle bonus from attacker to defender.

    :param attacker:
    :param defender:
    :return: a tuple, index 0 represents dmg bonus/loss, index 1 represents avoid bonus/loss
    """
    if attacker.inventory[0].item_type == ItemType.WEAPON and defender.inventory[0].item_type == ItemType.WEAPON:
        return weapon_triangle_bonus(attacker.inventory[0], defender.inventory[0])
    elif attacker.inventory[0].item_type == ItemType.TOME and defender.inventory[0].item_type == ItemType.TOME:
        return magic_triangle_bonus(attacker.inventory[0], defender.inventory[0])

def calculate_crit_avoid(unit: Unit):
    """
    Calculates the chance that unit will "avoid" a critical hit
    :param unit:
    :return: a float that represents the chance that unit will avoid crit hits
    """
    return unit.luck / 100


def calculate_crit_rate(unit: Unit):
    """
    Calculates the critical hit rate of unit

    :param unit: the unit
    :return: A float that represents the critical hit rate of the unit
    """
    weapon_crit = unit.inventory[0].info['crit']
    crit_bonus = 0.0
    if 'Swordmaster' in unit.job or 'Berserker' in unit.job:
        crit_bonus = 0.15
    return weapon_crit + ((unit.skill / 100) / 2) + crit_bonus


def calculate_crit_chance(attacker: Unit, defender: Unit):
    """
    Main function used to calculate critical chance

    :param attacker: The unit who is attacking
    :param defender: The unit who is defending
    :return: The chance between 0.0 and 1.0 for attacker to hand a critical hit on defender
    """
    crit_rate = calculate_crit_rate(attacker)
    crit_avoid = calculate_crit_avoid(defender)
    return min(max(0, crit_rate - crit_avoid), 1.0)


def calculate_accuracy(attacker: Unit, defender: Unit):
    """
    Calculates the accuracy rate of attacker against defender

    :param attacker: The unit who is we are calculating accuracy rate for
    :param defender: The unit who is defending
    :return: A number between 0.0 and 1.0 that shows how accurate a given attack will be
    """
    triangle_accuracy_bonus = calculate_triangle_bonus(attacker, defender)[1]
    weapon_hit = attacker.inventory[0].info['hit']
    return weapon_hit + ((attacker.skill / 100) * 2) + ((attacker.luck / 100) / 2) + triangle_accuracy_bonus


def calculate_attack_speed(unit: Unit):
    weapon_weight = unit.inventory[0].info['weight']
    return unit.speed - (max(weapon_weight - unit.con, 0))


def calculate_might(attacker: Unit, defender: Unit, tile_map: Map):
    """
    Calculates the damage that attacker would do to defender on tile_map in combat.

    :param attacker: The unit who is initiating the attack
    :param defender: The unit who is defending from attacker's attack
    :param tile_map: The map this combat is taking place on
    :return: A integer that describes how much HP the defender will lose in combat against attacker
    """
    triangle_bonus = calculate_triangle_bonus(attacker, defender)

    if attacker.inventory[0].item_type == ItemType.WEAPON:
        attack = attacker.strength + (attacker.inventory[0].info['might'] + triangle_bonus[0])
        defense = defender.defense + tile_map.get_tile(defender.x, defender.y).defense
    else:
        attack = attacker.magic + (attacker.inventory[0].info['might'] + triangle_bonus[0])
        defense = defender.res + tile_map.get_tile(defender.x, defender.y).defense

    return attack - defense


def calculate_avoid(unit: Unit, tile_map: Map):
    """
    Calculates the chance for unit to avoid a given attack
    :param unit: The unit who we are calculating avoidance rate
    :param tile_map: The map the unit exists on
    :return: A number between 0.0 and 1.0 that represents the avoidance rate of unit
    """
    attack_speed = calculate_attack_speed(unit)
    terrain_avoid_bonus = tile_map.get_tile(unit.x, unit.y).avoid
    return ((attack_speed * 2) / 100) + (unit.luck / 100) + terrain_avoid_bonus


def calculate_hit_chance(attacker: Unit, defender: Unit, tile_map: Map):
    """
    Main function used to calculate the chance that attacker will hit defender on tile_map
    If the attacker's range is less than the defenders range, then the hit chance will be zero

    :param attacker: The unit who is attacking
    :param defender: The unit who is defending
    :param tile_map: The map in which the combat is taking place
    :return: The chance between 0.0 and 1.0 for attacker to hit defender in combat
    """
    distance = tile_map.manhattan_distance(attacker.x, attacker.y, defender.x, defender.y)
    atk_range = list(attacker.inventory[0].info['range'].split(','))

    if str(distance) not in atk_range:
        return 0.0

    accuracy = calculate_accuracy(attacker, defender)
    avoid = calculate_avoid(defender, tile_map)
    return min(max(0.0, accuracy - avoid), 1.0)


def get_combat_stats(attacker: Unit, defender: Unit, tile_map: Map):
    """
    Calculates the battle stats between attacker and defender on map tile_map

    :param attacker: The unit who is initiating combat. Whoever initiates always attacks first.
    :param defender: The unit who is defending in combat.
    :param tile_map: The map that the unit's battle is taking place on
    :return: A CombatSummary object that describes the battle that would take place between attacker and defender
    """
    attacker_hit_chance = calculate_hit_chance(attacker, defender, tile_map)
    attacker_might = calculate_might(attacker, defender, tile_map)
    attacker_crit_chance = calculate_crit_chance(attacker, defender)
    attacker_doubling = False

    defender_hit_chance = calculate_hit_chance(defender, attacker, tile_map)
    defender_might = calculate_might(defender, attacker, tile_map)
    defender_crit_chance = calculate_crit_chance(defender, attacker)
    defender_doubling = False

    attacker_as = calculate_attack_speed(attacker)
    defender_as = calculate_attack_speed(defender)
    attacker_as_dif = attacker_as - defender_as
    defender_as_dif = defender_as - attacker_as

    if attacker_as_dif >= 4:
        attacker_doubling = True

    if defender_as_dif >= 4:
        defender_doubling = True

    attacker_combat = Combat(attacker_hit_chance, attacker_might, attacker_crit_chance, attacker_doubling)
    defender_combat = Combat(defender_hit_chance, defender_might, defender_crit_chance, defender_doubling)
    return CombatSummary(attacker, defender, attacker_combat, defender_combat)


def roll_random_chance():
    """
    Averages two random floats between 0.0 and 1.0, n and k

    Something interesting to note about Fire Emblem combat randomness, from the FE wiki:

    "Note that in all games starting from Fire Emblem: The Binding Blade, the Random Number Generator generates
    two numbers instead of one for hit chance, and the average of the numbers is the true hit value; in other words,
    a displayed hit (hit shown on screen) of 75 will actually hit on any two numbers whose average is less than or equal
    to 75. The effect on overall accuracy of attacks makes a sigmoid effect: it becomes exceedingly rare for an
    accurate attack (90+ hit) to miss, while inaccurate attacks (Hit lesser than 50) will land far less often
    than its hit rate would suggest"


    :return: A float between 0.0 and 1.0, with the above statement in mind
    """
    n = random.random()
    k = random.random()
    return (n + k) / 2


def simulate_combat(summary: CombatSummary):
    """
    Simulates the combat between two units

    :param summary: The CombatSummary generated from get_combat_stats
    :return:
    """
    # Hit 1
    hit_chance = roll_random_chance()
    if hit_chance <= summary.attacker_summary.hit_chance:
        dmg = summary.attacker_summary.might

        crit_chance = roll_random_chance()
        if crit_chance <= summary.attacker_summary.crit_chance:
            dmg *= 3

        summary.defender.take_dmg(dmg)

    if summary.defender.current_hp <= 0:
        return CombatResults.DEFENDER_DEATH

    # Hit 2
    hit_chance = roll_random_chance()
    if hit_chance <= summary.defender_summary.hit_chance:
        dmg = summary.defender_summary.might

        crit_chance = roll_random_chance()
        if crit_chance <= summary.defender_summary.crit_chance:
            dmg *= 3

        summary.attacker.take_dmg(dmg)

    if summary.attacker.current_hp <= 0:
        return CombatResults.ATTACKER_DEATH

    # Hit 3
    if summary.attacker_summary.doubling:
        hit_chance = roll_random_chance()
        if hit_chance <= summary.attacker_summary.hit_chance:
            dmg = summary.attacker_summary.might

            crit_chance = roll_random_chance()
            if crit_chance <= summary.attacker_summary.crit_chance:
                dmg *= 3

            summary.defender.take_dmg(dmg)

        if summary.defender.current_hp <= 0:
            return CombatResults.DEFENDER_DEATH

    # Hit 4
    if summary.defender_summary.doubling:
        hit_chance = roll_random_chance()
        if hit_chance <= summary.defender_summary.hit_chance:
            dmg = summary.defender_summary.might

            crit_chance = roll_random_chance()
            if crit_chance <= summary.defender_summary.crit_chance:
                dmg *= 3

            summary.attacker.take_dmg(dmg)

        if summary.attacker.current_hp <= 0:
            return CombatResults.ATTACKER_DEATH

    return CombatResults.NO_DEATH
