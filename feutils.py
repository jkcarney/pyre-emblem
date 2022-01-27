def class_table(class_code):
    class_dict = {
        0x01B0: 'Lord', 0x0204: 'Lord', 0x0258: 'Lord', 0x03A8: 'Knight Lord', 0x03FC: 'Blade Lord',
        0x0450: 'Great Lord', 0x04A4: 'Mercenary', 0x04F8: 'Mercenary', 0x054C: 'Hero', 0x05A0: 'Hero',
        0x05F4: 'Myrmidon', 0x0648: 'Myrmidon', 0x069C: 'Swordmaster', 0x06F0: 'Swordmaster', 0x0744: 'Fighter',
        0x0798: 'Warrior', 0x07EC: 'Knight', 0x0840: 'Knight', 0x0894: 'General', 0x08E8: 'General', 0x093C: 'Archer',
        0x0990: 'Archer', 0x09E4: 'Sniper', 0x0A38: 'Sniper', 0x0A8C: 'Monk', 0x0AE0: 'Cleric', 0x0B34: 'Bishop',
        0x0B88: 'Bishop', 0x0BDC: 'Mage', 0x0C30: 'Mage', 0x0C84: 'Sage', 0x0CD8: 'Sage', 0x0D2C: 'Shaman',
        0x0D80: 'Shaman', 0x0DD4: 'Druid', 0x0E28: 'Druid', 0x0E7C: 'Cavalier', 0x0ED0: 'Cavalier', 0x0F24: 'Paladin',
        0x0F78: 'Paladin', 0x0FCC: 'Troubadour', 0x1020: 'Valkyrie', 0x1074: 'Nomad', 0x10c8: 'Nomad',
        0x111c: 'Nomad Trooper', 0x1170: 'Nomad Trooper', 0x11c4: 'Pegasus Knight', 0x1218: 'Falcoknight',
        0x126c: 'Wyvern Rider', 0x12c0: 'Wyvern Rider', 0x1314: 'Wyvern Lord', 0x1368: 'Wyvern Lord', 0x13bc: 'Soldier',
        0x1410: 'Brigand', 0x1464: 'Pirate', 0x14b8: 'Berserker', 0x150c: 'Thief', 0x1560: 'Thief', 0x15b4: 'Assassin',
        0x165c: 'Dancer', 0x16b0: 'Bard', 0x1704: 'Archsage', 0x1758: 'Magic Seal', 0x17ac: 'Tent',
        0x1800: 'Dark Druid', 0x1854: 'Fire Dragon'
    }

    return class_dict[class_code]


def constitution_table(character_code):
    """
    Retrieves the constitution of a character based on the character code.

    :param character_code:
    :return:
    """
    pass


def movement_table(job):
    """
    Retrieves the movement of the job passed in

    :param job:
    :return:
    """
    pass
