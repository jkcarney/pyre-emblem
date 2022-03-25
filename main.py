import environment
import unit_populator
from termcolor import colored


def main():
    n = 10000  # iterations
    env = environment.Environment()

    for x in range(n):
        print(colored(f'================ GAME {x} ================', 'green', 'on_grey'))

        # Environment resetting has a (small) probabilistic chance to fail; mainly just when generating maps.
        # For example, if there are no valid corners.
        # Or if the corner chosen only has a grass tile and water surrounding
        # This is a bit of a hack, but given my limited timeframe, heck it :)
        valid = False
        blue_team = []
        red_team = []

        while not valid:
            try:
                env.reset()
                blue_team = unit_populator.generate_blue_team(env.map)
                red_team = unit_populator.generate_red_team(env.map, blue_team)
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

                if len(red_team) == 0:
                    done = True
                    info['winner'] = 'Blue'
                    info['method'] = 'Killed all red units'

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

            if len(red_team) == 0:
                done = True
                info['winner'] = 'Blue'
                info['method'] = 'Killed all red units'

        # Save Q-Tables to disk after episode
        for unit in blue_team:
            unit.close()

    print('Done!')


if __name__ == "__main__":
    main()
