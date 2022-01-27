import feutils


class Unit:
    def __init__(self, character_code, x, y, level, job_code, hp_max,
                 strength, skill, spd, luck, defense, res):
        self.character_code = character_code
        self.x = x
        self.y = y
        self.level = level
        self.job = feutils.class_table(job_code)
        self.hp_max = hp_max
        self.current_hp = hp_max
        self.strength = strength
        self.skill = skill
        self.speed = spd
        self.luck = luck
        self.defense = defense
        self.res = res
        self.constitution = feutils.constitution_table(character_code)
        self.move = feutils.movement_table(self.job)