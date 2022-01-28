_character_dict = {
    0xce4c: 'Eliwood', 0xce80: 'Hector', 0xceb4: 'Lyn', 0xcee8: 'Raven', 0xcf1c: 'Geitz',
    0xcf50: 'Guy', 0xcf84: 'Karel', 0xcfb8: 'Dorcas', 0xcfec: 'Bartre', 0xd020: 'Citizen',
    0xd054: 'Oswin', 0xd088: 'Fargus', 0xd0bc: 'Wil', 0xd0f0: 'Rebecca', 0xd124: 'Louise',
    0xd158: 'Lucius', 0xd18c: 'Serra', 0xd1c0: 'Renault', 0xd1f4: 'Erk', 0xd228: 'Nino',
    0xd25c: 'Pent', 0xd290: 'Canas', 0xd2c4: 'Kent', 0xd2f8: 'Sain', 0xd32c: 'Lowen',
    0xd360: 'Marcus', 0xd394: 'Priscilla', 0xd3c8: 'Rath', 0xd3fc: 'Florina',
    0xd430: 'Fiora', 0xd464: 'Farina', 0xd498: 'Heath', 0xd4cc: 'Vaida', 0xd500: 'Hawkeye',
    0xd534: 'Matthew', 0xd568: 'Jaffar', 0xd59c: 'Ninian', 0xd5d0: 'Nils', 0xd604: 'Athos',
    0xd638: 'Merlinus', 0xd66c: 'Nils', 0xd6a0: 'Uther', 0xd6d4: 'Vaida',
    0xd708: 'Wallace', 0xd73c: 'Lyn', 0xd770: 'Wil', 0xd7a4: 'Kent', 0xd7d8: 'Sain',
    0xd80c: 'Florina', 0xd840: 'Rath', 0xd874: 'Dart', 0xd8a8: 'Isadora',
    0xd8dc: 'Eleanora', 0xd910: 'Legault', 0xd944: 'Karla',
    0xd978: 'Harken', 0xd9ac: 'Leila', 0xd9e0: 'Bramimond',
    0xda14: 'Kishuna', 0xda48: 'Groznyi', 0xda7c: 'Wire', 0xdab0: 'Bandit', 0xdae4: 'Zagan',
    0xdb18: 'Boies', 0xdb4c: 'Puzon', 0xdb80: 'Bandit', 0xdbb4: 'Santals',
    0xdbe8: 'Nergal', 0xdc1c: 'Erik', 0xdc50: 'Sealen', 0xdc84: 'Bauker', 0xdcb8: 'Bernard',
    0xdcec: 'Damian', 0xdd20: 'Zoldam', 0xdd54: 'Uhai', 0xdd88: 'Aion', 0xddbc: 'Darin',
    0xddf0: 'Cameron', 0xde24: 'Oleg', 0xde58: 'Eubans', 0xde8c: 'Ursula',
    0xdec0: 'Black Fang', 0xdef4: 'Paul', 0xdf28: 'Jasmine', 0xdf5c: 'Black Fang',
    0xdf90: 'Jerme', 0xdfc4: 'Pascal', 0xdff8: 'Kenneth', 0xe02c: 'Jerme',
    0xe060: 'Maxime', 0xe094: 'Sonia', 0xe0c8: 'Teodor', 0xe0fc: 'Georg',
    0xe130: 'Kaim', 0xe164: 'Merc', 0xe198: 'Denning', 0xe1cc: 'Bern', 0xe200: 'Morph',
    0xe234: 'Lloyd', 0xe268: 'Linus', 0xe29c: 'Lloyd', 0xe2d0: 'Linus', 0xe304: 'Bandit',
    0xe338: 'Bandit', 0xe36c: 'Bandit', 0xe3a0: 'Laus', 0xe3d4: 'Laus', 0xe408: 'Pirate',
    0xe43c: 'Black Fang', 0xe470: 'Black Fang', 0xe4a4: 'Ostia', 0xe4d8: 'Black Fang',
    0xe50c: 'Guardian', 0xe540: 'Morph', 0xe574: 'Morph', 0xe5a8: 'Morph', 0xe5dc: 'Caelin',
    0xe610: 'Caelin', 0xe644: 'Caelin', 0xe678: 'Laus', 0xe6ac: 'Laus', 0xe6e0: 'Zephiel',
    0xe714: 'Elbert', 0xe748: 'Black Fang', 0xe77c: 'Black Fang',
    0xe7b0: 'Black Fang', 0xe7e4: 'Morph', 0xe818: 'Morph', 0xe84c: 'Morph',
    0xe880: 'Morph', 0xe8b4: 'Black Fang', 0xe8e8: 'Brendan', 0xe91c: 'Limstella',
    0xe950: 'Dragon', 0xe984: 'Batta', 0xe9b8: 'Bandit', 0xe9ec: 'Zugu', 0xea20: 'Bandit',
    0xea54: 'Bandit', 0xea88: 'Bandit', 0xeabc: 'Glass', 0xeaf0: 'Migal', 0xeb24: 'Bandit',
    0xeb58: 'Bandit', 0xeb8c: 'Bandit', 0xebc0: 'Bandit', 0xebf4: 'Bandit',
    0xec28: 'Carjiga', 0xec5c: 'Bandit', 0xec90: 'Bandit', 0xecc4: 'Bandit',
    0xecf8: 'Bandit', 0xed2c: 'Bug', 0xed60: 'Bandit', 0xed94: 'Bandit', 0xedc8: 'Bandit',
    0xedfc: 'Bandit', 0xee30: 'Natalie', 0xee64: 'Bool', 0xee98: 'Bandit',
    0xeecc: 'Bandit', 0xef00: 'Bandit', 0xef34: 'Bandit', 0xef68: 'Bandit',
    0xef9c: 'Bandit', 0xefd0: 'Heintz', 0xf004: 'Black Fang', 0xf038: 'Black Fang',
    0xf06c: 'Black Fang', 0xf0a0: 'Black Fang', 0xf0d4: 'Black Fang', 0xf108: 'Black Fang',
    0xf13c: 'Beyard', 0xf170: 'Black Fang', 0xf1a4: 'Black Fang', 0xf1d8: 'Black Fang',
    0xf20c: 'Black Fang', 0xf240: 'Black Fang', 0xf274: 'Black Fang', 0xf2a8: 'Black Fang',
    0xf2dc: 'Black Fang', 0xf310: 'Yogi', 0xf344: 'Caelin', 0xf378: 'Caelin',
    0xf3ac: 'Caelin', 0xf3e0: 'Caelin', 0xf414: 'Caelin', 0xf448: 'Caelin',
    0xf47c: 'Caelin', 0xf4b0: 'Eagler', 0xf4e4: 'Caelin', 0xf518: 'Caelin',
    0xf54c: 'Caelin', 0xf580: 'Caelin', 0xf5b4: 'Caelin', 0xf5e8: 'Caelin',
    0xf61c: 'Lundgren', 0xf650: 'Caelin', 0xf684: 'Caelin', 0xf6b8: 'Caelin',
    0xf6ec: 'Caelin', 0xf720: 'Caelin', 0xf754: 'Caelin', 0xf788: 'Caelin',
    0xf7bc: 'Tactician', 0xf7f0: 'Citizen', 0xf824: 'Citizen', 0xf858: 'Citizen',
    0xf88c: 'Citizen', 0xf8c0: 'Citizen', 0xf8f4: 'Citizen', 0xf928: 'Citizen',
    0xf95c: 'Citizen', 0xf990: 'Citizen', 0xf9c4: 'Merc', 0xf9f8: 'Pirate',
    0xfa2c: 'Bandit', 0xfa60: 'Citizen', 0xfa94: 'Citizen', 0xfac8: 'Citizen',
    0xfafc: 'Black Fang', 0xfb30: 'Black Fang', 0xfb64: 'Bandit', 0xfb98: 'Black Fang',
    0xfbcc: 'Morph', 0xfc00: 'Black Fang', 0xfc34: 'Black Fang', 0xfc68: 'Bandit',
    0xfc9c: 'Ostia', 0xfcd0: "Rath's unit", 0xfd04: 'Bandit', 0xfd38: 'Bandit',
    0xfd6c: 'Bern', 0xfda0: 'Guardian', 0xfdd4: 'Morph', 0xfe08: 'Laus',
    0xfe3c: 'Bandit', 0xfe70: 'Bandit', 0xfea4: 'Bern', 0xfed8: 'Guardian',
    0xff0c: 'Morph', 0xff40: 'Guardian', 0xff74: 'Black Fang',
    0xffa8: 'Lloyd', 0xffdc: 'Linus'
}

_item_dict = {
    0x0: 'Nothing', 0x1: 'Iron Sword', 0x2: 'Slim Sword', 0x3: 'Steel Sword', 0x4: 'Silver Sword',
    0x5: 'Iron Blade', 0x6: 'Steel Blade', 0x7: 'Silver Blade', 0x8: 'Poison Sword', 0x9: 'Rapier',
    0xa: 'Mani Katti', 0xb: 'Brave Sword', 0xc: 'Wo Dao', 0xd: 'Killing Edge', 0xe: 'Armorslayer',
    0xf: 'Wyrmslayer', 0x10: 'Light Brand', 0x11: 'Runesword', 0x12: 'Lancereaver', 0x13: 'Longsword',
    0x14: 'Iron Lance', 0x15: 'Slim Lance', 0x16: 'Steel Lance', 0x17: 'Silver Lance', 0x18: 'Poison Lance',
    0x19: 'Brave Lance', 0x1a: 'Killer Lance', 0x1b: 'Horseslayer', 0x1c: 'Javelin', 0x1d: 'Spear',
    0x1e: 'Axereaver', 0x1f: 'Iron Axe', 0x20: 'Steel Axe', 0x21: 'Silver Axe', 0x22: 'Poison Axe',
    0x23: 'Brave Axe', 0x24: 'Killer Axe', 0x25: 'Halberd', 0x26: 'Hammer', 0x27: 'Devil Axe',
    0x28: 'Hand Axe', 0x29: 'Tomahawk', 0x2a: 'Swordreaver', 0x2b: 'Swordslayer', 0x2c: 'Iron Bow',
    0x2d: 'Steel Bow', 0x2e: 'Silver Bow', 0x2f: 'Poison Bow', 0x30: 'Killer Bow', 0x31: 'Brave Bow',
    0x32: 'Short Bow', 0x33: 'Long Bow', 0x34: 'Ballista', 0x35: 'Iron ballista', 0x36: 'Killer ballista',
    0x37: 'Fire', 0x38: 'Thunder', 0x39: 'Elfire', 0x3a: 'Bolting', 0x3b: 'Fimbulvetr', 0x3c: 'Forblaze',
    0x3d: 'Excalibur', 0x3e: 'Lightning', 0x3f: 'Shine', 0x40: 'Divine', 0x41: 'Purge', 0x42: 'Aura',
    0x43: 'Luce', 0x44: 'Flux', 0x45: 'Luna', 0x46: 'Nosferatu', 0x47: 'Eclipse', 0x48: 'Fenrir',
    0x49: 'Gespenst', 0x4a: 'Heal', 0x4b: 'Mend', 0x4c: 'Recover', 0x4d: 'Physic', 0x4e: 'Fortify',
    0x4f: 'Restore', 0x50: 'Silence', 0x51: 'Sleep', 0x52: 'Berserk', 0x53: 'Warp', 0x54: 'Rescue',
    0x55: 'Torch', 0x56: 'Hammerne', 0x57: 'Unlock', 0x58: 'Barrier', 0x59: 'Dragon Axe', 0x5a: 'Angelic robe',
    0x5b: 'Energy ring', 0x5c: 'Secret book', 0x5d: 'Speedwings', 0x5e: 'Goddess icon', 0x5f: 'Dragonshield',
    0x60: 'Talisman', 0x61: 'Boots', 0x62: 'Body ring', 0x63: 'Hero crest', 0x64: 'Knight crest',
    0x65: "Orion's bolt", 0x66: 'Elysian whip', 0x67: 'Guiding ring', 0x68: 'Chest key', 0x69: 'Door key',
    0x6a: 'Lockpick', 0x6b: 'Vulnerary', 0x6c: 'Elixir', 0x6d: 'Pure water', 0x6e: 'Antitoxin',
    0x6f: 'Torch', 0x70: 'Delphi Shield', 0x71: 'Member Card', 0x72: 'Silver Card', 0x73: 'White gem',
    0x74: 'Blue gem', 0x75: 'Red gem', 0x77: "Vaida's Spear", 0x78: 'Chest key', 0x79: 'Mine',
    0x7a: 'Light rune', 0x7b: 'Iron rune', 0x7c: "Filla's Might", 0x7d: "Ninis's Grace", 0x7e: "Thor's Ire",
    0x7f: "Set's Litany", 0x80: 'Emblem blade', 0x81: 'Emblem lance', 0x82: 'Emblem axe', 0x83: 'Emblem bow',
    0x84: 'Durandal', 0x85: 'Armads', 0x86: 'Aureola', 0x87: 'Earth seal', 0x88: "Afa's Drops",
    0x89: 'Heaven seal', 0x8a: 'Emblem seal', 0x8b: 'Fell contract', 0x8c: 'Sol Katti', 0x8d: 'Wolf Beil',
    0x8e: 'Ereshkigal', 0x8f: 'Flametongue', 0x90: 'Regal blade', 0x91: 'Rex Hasta', 0x92: 'Basilikos',
    0x93: 'Reinfleche', 0x94: 'Heavy spear', 0x95: 'Short spear', 0x96: 'Ocean seal', 0x99: 'Wind Sword'
}

_class_dict = {
    0x1b0: 'Lord (Eliwood)', 0x204: 'Lord (Lyn)', 0x258: 'Lord (Hector)', 0x3a8: 'Knight Lord', 0x3fc: 'Blade Lord',
    0x450: 'Great Lord', 0x4a4: 'Mercenary',
    0x54c: 'Male Hero', 0x5a0: 'Female Hero',
    0x5f4: 'Male Myrmidon', 0x648: 'Female Myrmidon',
    0x69c: 'Male Swordmaster', 0x6f0: 'Female Swordmaster',
    0x744: 'Fighter', 0x798: 'Warrior',
    0x7ec: 'Male Knight', 0x840: 'Female Knight', 0x894: 'Male General', 0x8e8: 'Female General',
    0x93c: 'Male Archer', 0x990: 'Female Archer', 0x9e4: 'Male Sniper', 0xa38: 'Female Sniper',
    0xa8c: 'Monk', 0xae0: 'Cleric', 0xb34: 'Male Bishop', 0xb88: 'Female Bishop',
    0xbdc: 'Male Mage', 0xc30: 'Female Mage', 0xc84: 'Male Sage', 0xcd8: 'Female Sage',
    0xd2c: 'Male Shaman', 0xd80: 'Female Shaman', 0xdd4: 'Male Druid', 0xe28: 'Female Druid',
    0xe7c: 'Male Cavalier', 0xed0: 'Female Cavalier', 0xf24: 'Male Paladin', 0xf78: 'Female Paladin',
    0xfcc: 'Troubadour', 0x1020: 'Valkyrie',
    0x1074: 'Male Nomad', 0x10c8: 'Female Nomad', 0x111c: 'Male Nomad Trooper', 0x1170: 'Female Nomad Trooper',
    0x11c4: 'Pegasus Knight', 0x1218: 'Falcoknight',
    0x126c: 'Male Wyvern Rider', 0x12c0: 'Female Wyvern Rider',
    0x1314: 'Male Wyvern Lord', 0x1368: 'Female Wyvern Lord',
    0x13bc: 'Soldier',
    0x1410: 'Brigand', 0x1464: 'Pirate', 0x14b8: 'Berserker',
    0x150c: 'Male Thief', 0x1560: 'Female Thief', 0x15b4: 'Assassin',
    0x165c: 'Dancer', 0x16b0: 'Bard', 0x1704: 'Archsage', 0x1758: 'Magic Seal', 0x17ac: 'Tent', 0x1800: 'Dark Druid',
    0x1854: 'Fire Dragon', 0x19a4: 'Bramimond', 0x1b9c: 'Corsair', 0x1E90: 'Wagon'
}

_movement_dict = {
    'Lord (Eliwood)': 5, 'Lord (Lyn)': 5, 'Lord (Hector)': 5,
    'Blade Lord': 6, 'Knight Lord': 7, 'Great Lord': 5,
    'Bard': 5, 'Dancer': 5, 'Prince': 5,
    'Tent': 0, 'Wagon': 5, 'Soldier': 5,
    'Male Cavalier': 7, 'Female Cavalier': 7,
    'Male Paladin': 8, 'Female Paladin': 8,
    'Male Knight': 4, 'Female Knight': 4,
    'Male General': 5, 'Female General': 5,
    'Male Mercenary': 5, 'Female Mercenary': 5,
    'Male Hero': 6, 'Female Hero': 6,
    'Male Myrmidon': 5, 'Female Myrmidon': 5,
    'Male Swordmaster': 6, 'Female Swordmaster': 6,
    'Male Thief': 6, 'Female Thief': 6,
    'Assassin': 6,
    'Male Archer': 5, 'Female Archer': 5,
    'Male Sniper': 6, 'Female Sniper': 6,
    'Male Nomad': 7, 'Female Nomad': 7,
    'Male Nomad Trooper': 7, 'Female Nomad Trooper': 7,
    'Male Wyvern Rider': 7, 'Female Wyvern Rider': 7,
    'Male Wyvern Lord': 8, 'Female Wyvern Lord': 8,
    'Male Mage': 5, 'Female Mage': 5,
    'Male Sage': 6, 'Female Sage': 6,
    'Monk': 5, 'Cleric': 5,
    'Male Bishop': 6, 'Female Bishop': 6,
    'Male Shaman': 5, 'Female Shaman': 5,
    'Male Druid': 6, 'Female Druid': 6,
    'Fighter': 5, 'Warrior': 6, 'Brigand': 5, 'Pirate': 5, 'Corsair': 5, 'Berserker': 6,
    'Pegasus Knight': 7, 'Falcoknight': 8, 'Troubadour': 7, 'Valkyrie': 8, 'Magic Seal': 6,
    'Archsage': 6, 'Dark Druid': 6, 'Bramimond': 5, 'Fire Dragon': 0
}

_character_constitution_dict = {
    'Lyn': 5, 'Sain': 9, 'Kent': 9, 'Florina': 4, 'Wil': 6, 'Dorcas': 14, 'Serra': 4, 'Erk': 5, 'Rath': 8, 'Matthew': 7,
    'Nils': 3, 'Lucius': 6, 'Wallace': 15, 'Eliwood': 7, 'Lowen': 10, 'Marcus': 11, 'Rebecca': 5, 'Bartre': 13,
    'Hector': 13, 'Oswin': 14, 'Guy': 5, 'Merlinus': 25, 'Priscilla': 4, 'Raven': 8, 'Lucius': 6, 'Canas': 7,
    'Dart': 10, 'Fiora': 5, 'Legault': 9, 'Ninian': 4, 'Isadora': 6, 'Heath': 9, 'Hawkeye': 16, 'Geitz': 13,
    'Farina': 5, 'Pent': 8, 'Louise': 6, 'Karel': 9, 'Harken': 11, 'Nino': 3, 'Jaffar': 8, 'Vaida': 12, 'Karla': 7,
    'Renault': 9, 'Athos': 9
}

_job_constitution_dict = {
    'Lord (Eliwood)': 5, 'Lord (Lyn)': 7, 'Lord (Hector)': 13,
    'Blade Lord': 6, 'Knight Lord': 9, 'Great Lord': 15,
    'Bard': 3, 'Dancer': 4, 'Prince': 7,
    'Tent': 25, 'Wagon': 25, 'Soldier': 6,
    'Male Cavalier': 9, 'Female Cavalier': 9,
    'Male Paladin': 11, 'Female Paladin': 9,
    'Male Knight': 13, 'Female Knight': 10,
    'Male General': 15, 'Female General': 11,
    'Male Mercenary': 9, 'Female Mercenary': 8,
    'Male Hero': 10, 'Female Hero': 9,
    'Male Myrmidon': 8, 'Female Myrmidon': 5,
    'Male Swordmaster': 9, 'Female Swordmaster': 7,
    'Male Thief': 6, 'Female Thief': 5,
    'Assassin': 6,
    'Male Archer': 7, 'Female Archer': 5,
    'Male Sniper': 8, 'Female Sniper': 6,
    'Male Nomad': 7, 'Female Nomad': 5,
    'Male Nomad Trooper': 8, 'Female Nomad Trooper': 6,
    'Male Wyvern Rider': 10, 'Female Wyvern Rider': 9,
    'Male Wyvern Lord': 11, 'Female Wyvern Lord': 10,
    'Male Mage': 6, 'Female Mage': 3,
    'Male Sage': 7, 'Female Sage': 4,
    'Monk': 6, 'Cleric': 4,
    'Male Bishop': 7, 'Female Bishop': 5,
    'Male Shaman': 7, 'Female Shaman': 3,
    'Male Druid': 8, 'Female Druid': 4,
    'Fighter': 11, 'Warrior': 13, 'Brigand': 12, 'Pirate': 10, 'Corsair': 10, 'Berserker': 13,
    'Pegasus Knight': 5, 'Falcoknight': 6, 'Troubadour': 5, 'Valkyrie': 6, 'Magic Seal': 7,
    'Archsage': 9, 'Dark Druid': 10, 'Bramimond': 6, 'Fire Dragon': 25
}


def class_table(class_code):
    # TODO: may need to make this more robust, ie it can accept hex code as string, int, w/e
    return _class_dict[class_code]


def item_table(item_code):
    # TODO: may need to make this more robust, ie it can accept hex code as string, int, w/e
    return _item_dict[item_code]


def character_constitution_table(character_name):
    """
    Gets the constitution of a character from their name
    Use this for playable characters
    :param character_name
    """
    # TODO: may need to make this more robust, ie it can accept hex code as string, int, w/e
    return _character_constitution_dict[character_name]


def job_constitution_table(job):
    """
    Gets the constituion of a character from the class bases
    Use this for enemy units
    :param job:
    :return:
    """
    return _job_constitution_dict[job]


def character_name_table(character_code):
    # TODO: may need to make this more robust, ie it can accept hex code as string, int, w/e
    return _character_dict[character_code]


def item_table(item_code):
    # TODO: may need to make this more robust, ie it can accept hex code as string, int, w/e
    return _item_dict[item_code]


def movement_table(job):
    return _movement_dict[job]
