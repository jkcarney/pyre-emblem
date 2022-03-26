import environment
import unit_populator
from termcolor import colored
import sys

n = 10000  # iterations


class FESimulationTypeError(Exception):
    pass


def main(simulation_mode):
    if simulation_mode == 'big':
        env = environment.Environment(18, 20, 18, 20)
        unit_factory = unit_populator.UnitFactory(5, 6, 15, 18)
    else:
        env = environment.Environment(6, 7, 6, 7)
        unit_factory = unit_populator.UnitFactory(2, 2, 5, 5)

    for x in range(n):
        print(colored(f'================ GAME {x} ================', 'green', 'on_grey'))

        # Environment resetting has a (small) probabilistic chance to fail; mainly just when generating maps.
        # For example, if there are no valid corners.
        # Or if the corner chosen only has a grass tile and water surrounding
        # This is a bit of a hack, but given my limited timeframe, heck it :)
        valid = False
        blue_team = []
        red_team = []
        info = {}

        while not valid:
            try:
                env.reset()
                blue_team = unit_factory.generate_blue_team(env.map)
                red_team = unit_factory.generate_red_team(env.map, blue_team)
                valid = True
            except:
                pass

        done = False

        while not done:
            print(colored('== BLUE PHASE ==', 'blue', 'on_white'))
            for agent in blue_team:
                state = env.obtain_state(agent, blue_team, red_team)
                action = agent.determine_action(state, env, blue_team, red_team)
                move = agent.determine_move(action, blue_team, red_team, env)

                next_state, reward, done, info = env.step(agent, move, action, blue_team, red_team)

                agent.update_qtable(state, next_state, reward, action)

                if len(blue_team) == 0:
                    done = True
                    info['winner'] = 'Red'
                    info['method'] = 'Killed all blue units'
                    env.red_victory = True

                if len(red_team) == 0:
                    done = True
                    info['winner'] = 'Blue'
                    info['method'] = 'Killed all red units'
                    env.blue_victory = True

                if done:
                    break

            if done:
                break

            print(colored('== RED PHASE ==', 'red', 'on_white'))
            _, done, info = env.execute_red_phase(blue_team, red_team)

            if len(blue_team) == 0:
                done = True
                info['winner'] = 'Red'
                info['method'] = 'Killed all blue units'
                env.red_victory = True

            if len(red_team) == 0:
                done = True
                info['winner'] = 'Blue'
                info['method'] = 'Killed all red units'
                env.blue_victory = True

        overall, ranks = env.obtain_metrics()
        print(colored('VICTORY RANK: ', 'yellow') + ranks[0])
        print('\t' + info['method'])
        print(colored('COMBAT RANK: ', 'yellow') + ranks[1])
        print(colored('SURVIVAL RANK: ', 'yellow') + ranks[2])
        print(colored('TACTIC RANK: ', 'yellow') + ranks[3])

        print(colored('OVERALL RANK: ', 'green') + overall)

        # Save Q-Tables to disk after episode
        for unit in blue_team:
            unit.close()

    print('Done!')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise FESimulationTypeError(f'Incorrect usage. Correct usage: python {sys.argv[0]} <mini or big>')

    arg = sys.argv[1].strip().lower()

    main(arg)
