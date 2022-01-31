import feutils
import item


class Unit:
    def __init__(self, character_code, x, y, level, job_code, hp_max,
                 strength, skill, spd, luck, defense, res, ally,
                 inventory_codes: list):
        self.character_code = character_code
        self.x = x
        self.y = y
        self.level = level
        self.hp_max = hp_max
        self.current_hp = hp_max
        self.strength = strength
        self.skill = skill
        self.speed = spd
        self.luck = luck
        self.defense = defense
        self.res = res

        self.inventory = item.construct_unit_inventory(inventory_codes)

        self.name = feutils.character_name_table(self.character_code)
        self.job = feutils.class_table(job_code)
        self.move = feutils.movement_table(self.job)

        if ally:
            self.con = feutils.character_constitution_table(self.name)
        else:
            self.con = feutils.job_constitution_table(self.job)


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

    def get_combat_stats(self, attacker: Unit, defender: Unit):
        pass
