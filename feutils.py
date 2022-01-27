def class_table(class_code):
    """
    Retrieves the class of a character from a class code

    :param class_code: the hexadecimal class code
    :return: The class as a string
    """
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


def character_name_table(character_code):
    """
    Retrieves the name of a character based on the character code
    :param character_code: the hexadecimal character code
    :return: the name of the associated character as a string
    """
    character_dict = {'0xce4c': 'Eliwood', '0xce80': 'Hector', '0xceb4': 'Lyn', '0xcee8': 'Raven', '0xcf1c': 'Geitz',
                      '0xcf50': 'Guy', '0xcf84': 'Karel', '0xcfb8': 'Dorcas', '0xcfec': 'Bartre', '0xd020': 'Citizen',
                      '0xd054': 'Oswin', '0xd088': 'Fargus', '0xd0bc': 'Wil', '0xd0f0': 'Rebecca', '0xd124': 'Louise',
                      '0xd158': 'Lucius', '0xd18c': 'Serra', '0xd1c0': 'Renault', '0xd1f4': 'Erk', '0xd228': 'Nino',
                      '0xd25c': 'Pent', '0xd290': 'Canas', '0xd2c4': 'Kent', '0xd2f8': 'Sain', '0xd32c': 'Lowen',
                      '0xd360': 'Marcus', '0xd394': 'Priscilla', '0xd3c8': 'Rath', '0xd3fc': 'Florina',
                      '0xd430': 'Fiora', '0xd464': 'Farina', '0xd498': 'Heath', '0xd4cc': 'Vaida', '0xd500': 'Hawkeye',
                      '0xd534': 'Matthew', '0xd568': 'Jaffar', '0xd59c': 'Ninian', '0xd5d0': 'Nils', '0xd604': 'Athos',
                      '0xd638': 'Merlinus', '0xd66c': 'Nils', '0xd6a0': 'Uther', '0xd6d4': 'Vaida',
                      '0xd708': 'Wallace', '0xd73c': 'Lyn', '0xd770': 'Wil', '0xd7a4': 'Kent', '0xd7d8': 'Sain',
                      '0xd80c': 'Florina', '0xd840': 'Rath', '0xd874': 'Dart', '0xd8a8': 'Isadora',
                      '0xd8dc': 'Eleanora', '0xd910': 'Legault', '0xd944': 'Karla',
                      '0xd978': 'Harken', '0xd9ac': 'Leila', '0xd9e0': 'Bramimond',
                      '0xda14': 'Kishuna', '0xda48': 'Groznyi', '0xda7c': 'Wire', '0xdab0': 'Bandit', '0xdae4': 'Zagan',
                      '0xdb18': 'Boies', '0xdb4c': 'Puzon', '0xdb80': 'Bandit', '0xdbb4': 'Santals',
                      '0xdbe8': 'Nergal', '0xdc1c': 'Erik', '0xdc50': 'Sealen', '0xdc84': 'Bauker', '0xdcb8': 'Bernard',
                      '0xdcec': 'Damian', '0xdd20': 'Zoldam', '0xdd54': 'Uhai', '0xdd88': 'Aion', '0xddbc': 'Darin',
                      '0xddf0': 'Cameron', '0xde24': 'Oleg', '0xde58': 'Eubans', '0xde8c': 'Ursula',
                      '0xdec0': 'Black Fang', '0xdef4': 'Paul', '0xdf28': 'Jasmine', '0xdf5c': 'Black Fang',
                      '0xdf90': 'Jerme', '0xdfc4': 'Pascal', '0xdff8': 'Kenneth', '0xe02c': 'Jerme',
                      '0xe060': 'Maxime', '0xe094': 'Sonia', '0xe0c8': 'Teodor', '0xe0fc': 'Georg',
                      '0xe130': 'Kaim', '0xe164': 'Merc', '0xe198': 'Denning', '0xe1cc': 'Bern', '0xe200': 'Morph',
                      '0xe234': 'Lloyd', '0xe268': 'Linus', '0xe29c': 'Lloyd', '0xe2d0': 'Linus', '0xe304': 'Bandit',
                      '0xe338': 'Bandit', '0xe36c': 'Bandit', '0xe3a0': 'Laus', '0xe3d4': 'Laus', '0xe408': 'Pirate',
                      '0xe43c': 'Black Fang', '0xe470': 'Black Fang', '0xe4a4': 'Ostia', '0xe4d8': 'Black Fang',
                      '0xe50c': 'Guardian', '0xe540': 'Morph', '0xe574': 'Morph', '0xe5a8': 'Morph', '0xe5dc': 'Caelin',
                      '0xe610': 'Caelin', '0xe644': 'Caelin', '0xe678': 'Laus', '0xe6ac': 'Laus', '0xe6e0': 'Zephiel',
                      '0xe714': 'Elbert', '0xe748': 'Black Fang', '0xe77c': 'Black Fang',
                      '0xe7b0': 'Black Fang', '0xe7e4': 'Morph', '0xe818': 'Morph', '0xe84c': 'Morph',
                      '0xe880': 'Morph', '0xe8b4': 'Black Fang', '0xe8e8': 'Brendan', '0xe91c': 'Limstella',
                      '0xe950': 'Dragon', '0xe984': 'Batta', '0xe9b8': 'Bandit', '0xe9ec': 'Zugu', '0xea20': 'Bandit',
                      '0xea54': 'Bandit', '0xea88': 'Bandit', '0xeabc': 'Glass', '0xeaf0': 'Migal', '0xeb24': 'Bandit',
                      '0xeb58': 'Bandit', '0xeb8c': 'Bandit', '0xebc0': 'Bandit', '0xebf4': 'Bandit',
                      '0xec28': 'Carjiga', '0xec5c': 'Bandit', '0xec90': 'Bandit', '0xecc4': 'Bandit',
                      '0xecf8': 'Bandit', '0xed2c': 'Bug', '0xed60': 'Bandit', '0xed94': 'Bandit', '0xedc8': 'Bandit',
                      '0xedfc': 'Bandit', '0xee30': 'Natalie', '0xee64': 'Bool', '0xee98': 'Bandit',
                      '0xeecc': 'Bandit', '0xef00': 'Bandit', '0xef34': 'Bandit', '0xef68': 'Bandit',
                      '0xef9c': 'Bandit', '0xefd0': 'Heintz', '0xf004': 'Black Fang', '0xf038': 'Black Fang',
                      '0xf06c': 'Black Fang', '0xf0a0': 'Black Fang', '0xf0d4': 'Black Fang', '0xf108': 'Black Fang',
                      '0xf13c': 'Beyard', '0xf170': 'Black Fang', '0xf1a4': 'Black Fang', '0xf1d8': 'Black Fang',
                      '0xf20c': 'Black Fang', '0xf240': 'Black Fang', '0xf274': 'Black Fang', '0xf2a8': 'Black Fang',
                      '0xf2dc': 'Black Fang', '0xf310': 'Yogi', '0xf344': 'Caelin', '0xf378': 'Caelin',
                      '0xf3ac': 'Caelin', '0xf3e0': 'Caelin', '0xf414': 'Caelin', '0xf448': 'Caelin',
                      '0xf47c': 'Caelin', '0xf4b0': 'Eagler', '0xf4e4': 'Caelin', '0xf518': 'Caelin',
                      '0xf54c': 'Caelin', '0xf580': 'Caelin', '0xf5b4': 'Caelin', '0xf5e8': 'Caelin',
                      '0xf61c': 'Lundgren', '0xf650': 'Caelin', '0xf684': 'Caelin', '0xf6b8': 'Caelin',
                      '0xf6ec': 'Caelin', '0xf720': 'Caelin', '0xf754': 'Caelin', '0xf788': 'Caelin',
                      '0xf7bc': 'Tactician', '0xf7f0': 'Citizen', '0xf824': 'Citizen', '0xf858': 'Citizen',
                      '0xf88c': 'Citizen', '0xf8c0': 'Citizen', '0xf8f4': 'Citizen', '0xf928': 'Citizen',
                      '0xf95c': 'Citizen', '0xf990': 'Citizen', '0xf9c4': 'Merc', '0xf9f8': 'Pirate',
                      '0xfa2c': 'Bandit', '0xfa60': 'Citizen', '0xfa94': 'Citizen', '0xfac8': 'Citizen',
                      '0xfafc': 'Black Fang', '0xfb30': 'Black Fang', '0xfb64': 'Bandit', '0xfb98': 'Black Fang',
                      '0xfbcc': 'Morph', '0xfc00': 'Black Fang', '0xfc34': 'Black Fang', '0xfc68': 'Bandit',
                      '0xfc9c': 'Ostia', '0xfcd0': "Rath's unit", '0xfd04': 'Bandit', '0xfd38': 'Bandit',
                      '0xfd6c': 'Bern', '0xfda0': 'Guardian', '0xfdd4': 'Morph', '0xfe08': 'Laus',
                      '0xfe3c': 'Bandit', '0xfe70': 'Bandit', '0xfea4': 'Bern', '0xfed8': 'Guardian',
                      '0xff0c': 'Morph', '0xff40': 'Guardian', '0xff74': 'Black Fang',
                      '0xffa8': 'Lloyd', '0xffdc': 'Linus'}
    print(character_dict[character_code])

def movement_table(job):
    """
    Retrieves the movement of the job passed in

    :param job:
    :return:
    """
    pass
