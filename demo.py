from matplotlib import colors, pyplot
import gym
import numpy as np

import unit
from unit import Unit
from map_factory import OutdoorMapFactory
import combat
import map
import item
import unit_populator


def action_in_valids(action, valid_actions):
    return np.any(np.all(action == valid_actions, axis=1))


if __name__ == "__main__":

    env = gym.make('fe_env:fe-env-v0')

    reward = 0

    blue_wins = 0
    red_wins = 0

    for x in range(100):
        print(f'=== Game {x} ===')
        env.reset()

        terminal = False

        while not terminal:
            valid = False
            random_action = env.action_space.sample()
            all_valid_actions = env.unwrapped.get_valid_actions_in_state()

            while not valid:
                if action_in_valids(random_action, all_valid_actions):
                    valid = True
                else:
                    random_action = env.action_space.sample()

            _, reward, terminal, _ = env.step(random_action)

        if reward == 100:
            blue_wins += 1
        elif reward == -100:
            red_wins += 1

    env.close()
    print(f'Blue Wins: {blue_wins} | Red Wins: {red_wins}')






    # map_factory = OutdoorMapFactory(10, 10, 10, 10)
    # fe_map,num_map = map_factory.generate_map()
    #
    # colormap = colors.ListedColormap(["green", "blue", "darkgreen", "brown"])
    #
    # valids = fe_map.get_valid_move_coordinates(lyn, [lyn], [bandit])
    #
    # print(valids)
    #
    # print(fe_map)
    #
    # pyplot.imshow(num_map,
    #               cmap=colormap,
    #               origin='upper',
    #               interpolation='none')
    # pyplot.show()
    #
    #     #print(fe_map)
    #
    #     #summary = combat.get_combat_stats(lyn, bandit, fe_map)
    #
    #     # print(f'{summary.attacker.name} {summary.attacker.current_hp}/{summary.attacker.hp_max}')
    #     # print('MT: ' + str(summary.attacker_summary.might))
    #     # print('HIT: ' + str(summary.attacker_summary.hit_chance))
    #     # print('CRIT: ' + str(summary.attacker_summary.crit_chance))
    #     # print('x2: ' + str(summary.attacker_summary.doubling))
    #     # print('\n-vs-\n')
    #     # print(f'{summary.defender.name} {summary.defender.current_hp}/{summary.defender.hp_max}')
    #     # print('MT: ' + str(summary.defender_summary.might))
    #     # print('HIT: ' + str(summary.defender_summary.hit_chance))
    #     # print('CRIT: ' + str(summary.defender_summary.crit_chance))
    #     # print('x2: ' + str(summary.defender_summary.doubling))
    #
    #     # print('\nSimulating combat...\n')
    # #     combat.simulate_combat(summary)
    # #
    # #     if summary.attacker.current_hp < 17:
    # #         lyn_hit_count += 1
    # #
    # # print('After ' + str(i) + ' iterations, Lyn got hit a simulated ' + str(lyn_hit_count) + ' times')
    # # print(str(lyn_hit_count / i) + ' hit rate')
