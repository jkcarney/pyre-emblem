import unit
from unit import Unit
from map_factory import OutdoorMapFactory
import combat
import map
import item

if __name__ == "__main__":

    lyn = Unit(0xceb4, 0, 0, 2, 0x0204, 17, 6, 8, 10, 6, 2, 0, 0, True, [0x1, 0x6b])
    bandit = Unit(0xe9b8, 0, 1, 2, 0x1410, 21, 4, 1, 4, 0, 3, 0, 0, False, [0x1f])

    map_factory = OutdoorMapFactory(10, 10, 10, 10)
    fe_map = map_factory.generate_map()[0]
    #print(fe_map)

    combat = combat.get_combat_stats(lyn, bandit, fe_map)

    print(combat.attacker.name)
    print('MT: ' + str(combat.attacker_summary.might))
    print('HIT: ' + str(combat.attacker_summary.hit_chance))
    print('CRIT: ' + str(combat.attacker_summary.crit_chance))
    print('x2: ' + str(combat.attacker_summary.doubling))
    print('\n-vs-\n')
    print(combat.defender.name)
    print('MT: ' + str(combat.defender_summary.might))
    print('HIT: ' + str(combat.defender_summary.hit_chance))
    print('CRIT: ' + str(combat.defender_summary.crit_chance))
    print('x2: ' + str(combat.defender_summary.doubling))
