from matplotlib import colors, pyplot

import unit
from unit import Unit
from map_factory import OutdoorMapFactory
import combat
import map
import item

if __name__ == "__main__":
    #lyn_hit_count = 0
    #for i in range(1001):
    lyn = Unit(0xceb4, 0, 0, 2, 0x0204, 17, 6, 8, 10, 6, 2, 0, 0, True, [0x1, 0x6b], True)
    bandit = Unit(0xe9b8, 0, 1, 2, 0x1410, 21, 4, 1, 4, 0, 3, 0, 0, False, [0x1f], False)

    map_factory = OutdoorMapFactory(10, 10, 10, 10)
    fe_map,num_map = map_factory.generate_map()

    colormap = colors.ListedColormap(["green", "blue", "darkgreen", "brown"])

    valids = fe_map.get_valid_move_coordinates(lyn)

    print(valids)

    print(fe_map)

    pyplot.imshow(num_map,
                  cmap=colormap,
                  origin='upper',
                  interpolation='none')
    pyplot.show()

        #print(fe_map)

        #summary = combat.get_combat_stats(lyn, bandit, fe_map)

        # print(f'{summary.attacker.name} {summary.attacker.current_hp}/{summary.attacker.hp_max}')
        # print('MT: ' + str(summary.attacker_summary.might))
        # print('HIT: ' + str(summary.attacker_summary.hit_chance))
        # print('CRIT: ' + str(summary.attacker_summary.crit_chance))
        # print('x2: ' + str(summary.attacker_summary.doubling))
        # print('\n-vs-\n')
        # print(f'{summary.defender.name} {summary.defender.current_hp}/{summary.defender.hp_max}')
        # print('MT: ' + str(summary.defender_summary.might))
        # print('HIT: ' + str(summary.defender_summary.hit_chance))
        # print('CRIT: ' + str(summary.defender_summary.crit_chance))
        # print('x2: ' + str(summary.defender_summary.doubling))

        # print('\nSimulating combat...\n')
    #     combat.simulate_combat(summary)
    #
    #     if summary.attacker.current_hp < 17:
    #         lyn_hit_count += 1
    #
    # print('After ' + str(i) + ' iterations, Lyn got hit a simulated ' + str(lyn_hit_count) + ' times')
    # print(str(lyn_hit_count / i) + ' hit rate')
