from enum import Enum


class ItemType(Enum):
    WEAPON = 0,
    STAFF = 1,
    TOME = 2,
    HEAL_CONSUMABLE = 3,
    NOTHING = 4,
    UNUSED = 5


class WeaponType(Enum):
    SWORD = 0,
    LANCE = 1,
    AXE = 2,
    BOW = 3


class TomeType(Enum):
    ANIMA = 0,
    LIGHT = 1,
    DARK = 2