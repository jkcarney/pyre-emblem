import feutils
import item
from item import Item
from item_type import *
from map import Map


class Unit:
    def __init__(self, character_code, x, y, level, job_code, hp_max,
                 strength, skill, spd, luck, defense, res, magic, ally,
                 inventory_codes: list, terminal_condition):
        self.terminal_condition = terminal_condition

        self.character_code = character_code
        self.x = x
        self.y = y
        self.level = level
        self.hp_max = hp_max
        self.current_hp = hp_max
        self.strength = strength
        self.magic = magic
        self.skill = skill
        self.speed = spd
        self.luck = luck
        self.defense = defense
        self.res = res

        self.inventory = item.construct_unit_inventory(inventory_codes)

        self.name = feutils.character_name_table(self.character_code)
        self.job = feutils.class_table(job_code)
        self.move = feutils.movement_table(self.job)
        self.terrain_group = feutils.job_terrain_group(self.job)

        if ally:
            self.con = feutils.character_constitution_table(self.name)
        else:
            self.con = feutils.job_constitution_table(self.job)

    def equip_item(self, index):
        self.inventory[0], self.inventory[index] = self.inventory[index], self.inventory[0]

    def get_attack_range(self):
        atk_range = set()

        for i in self.inventory:
            if item.item_type == ItemType.WEAPON or item.item_type == ItemType.TOME:
                item_ranges = list(map(int, i.info['range'].split(',')))
                for r in item_ranges:
                    atk_range.add(r)

        return sorted(list(atk_range))

    def has_consumable(self):
        for i in self.inventory:
            if i.item_type == ItemType.HEAL_CONSUMABLE:
                return True

        return False

    def get_all_consumables(self):
        consums = []
        for i in self.inventory:
            if i.item_type == ItemType.HEAL_CONSUMABLE:
                consums.append(i)

        return consums

    def goto(self, new_x, new_y):
        self.x, self.y = new_x, new_y

    def use_item(self, index):
        inventory_item = self.inventory[index]
        if inventory_item.item_type == ItemType.HEAL_CONSUMABLE:
            self.heal(inventory_item.info['heal_amount'])
            inventory_item.info['uses'] -= 1

            if inventory_item.info['uses'] == 0:
                del self.inventory[index]

            return True

        else:
            return False

    def heal(self, amount):
        self.current_hp = min(self.current_hp + amount, self.hp_max)

    def take_dmg(self, amount):
        self.current_hp -= amount

