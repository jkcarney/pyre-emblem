import environment
import unit_populator
from termcolor import colored
import fedata
import sys
from datetime import datetime
import logging

class FESimulationTypeError(Exception):
    pass


def game_over_check(blue_length, red_length, info, env):
    if blue_length == 0:
        info['winner'] = 'Red'
        info['method'] = 'Killed all blue units'
        env.red_victory = True
        return True  # Done?

    if red_length == 0:
        info['winner'] = 'Blue'
        info['method'] = 'Killed all red units'
        env.blue_victory = True
        return True  # Done?

    return False


def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = logging.FileHandler('exceptions.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def main(simulation_mode, run_name, iterations):
    if simulation_mode == 'big':
        env = environment.Environment(18, 20, 18, 20)
        unit_factory = unit_populator.UnitFactory(5, 6, 15, 18, run_name)
    else:
        env = environment.Environment(15, 15, 15, 15)
        unit_factory = unit_populator.UnitFactory(2, 2, 5, 5, run_name)

    # Establish SQLite database
    data_aggregator = fedata.FEData(run_name)

    for x in range(iterations):
        print(colored(f'================ GAME {x + 1} ================', 'green', 'on_grey'))
        start = datetime.now()

        # Environment resetting has a (small) probabilistic chance to fail; mainly just when generating maps.
        # For example, if there are no valid corners.
        # Or if the corner chosen only has a grass tile and water surrounding
        # This is a bit of a hack, but given my limited timeframe its a quick fix
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
        blue_team_names = []
        for unit in blue_team:
            blue_team_names.append(unit.name)

        while not done:
            print(colored('== BLUE PHASE ==', 'blue', 'on_white'))
            for agent in blue_team:
                state = env.obtain_state(agent, blue_team, red_team)
                action = agent.determine_action(state, env, blue_team, red_team)
                move = agent.determine_move(action, blue_team, red_team, env)

                # Save the history of state-actions in case of unit death
                agent.state_action_history.append(state + (action,))

                next_state, reward, done, info = env.step(agent, move, action, blue_team, red_team)

                agent.update_qtable(state, next_state, reward, action)

                if done:
                    break

                done = game_over_check(len(blue_team), len(red_team), info, env)

                if done:
                    break

            if done:
                break

            print(colored('== RED PHASE ==', 'red', 'on_white'))
            _, done, info = env.execute_red_phase(blue_team, red_team)

            if done:
                break

            done = game_over_check(len(blue_team), len(red_team), info, env)

        ranks = env.obtain_metrics()
        print(colored('VICTORY RANK: ', 'yellow') + ranks[0])
        print('\t' + info['method'])
        print(colored('SURVIVAL RANK: ', 'yellow') + str(ranks[1]))
        print(colored('TACTIC RANK: ', 'yellow') + str(ranks[2]))

        data_aggregator.add_entry(x, ranks[0], ranks[1], ranks[2], blue_team_names)

        # Save Q-Tables to disk after episode
        for unit in blue_team:
            unit.close()

        end = datetime.now()
        diff = end - start
        seconds = diff.total_seconds()
        print(colored(f"\nGame {x} took {seconds} seconds", 'yellow'))

    print('Done!')


if __name__ == "__main__":
    sys.stderr = sys.stdout
    logger = configure_logger()
    if len(sys.argv) != 4:
        raise FESimulationTypeError(f'Correct usage: python {sys.argv[0]} <mini or big> <run name> <iterations>')

    mini_arg = sys.argv[1].strip().lower()      # mini or big
    run_name_arg = sys.argv[2].strip().lower()  # run name (qtable and db file get the name)
    iterations = int(sys.argv[3])               # how many iterations to do (usually 200,000 is a decent starting point)

    simu_start = datetime.now()
    try:
        main(mini_arg, run_name_arg, iterations)
    except Exception as e:
        logger.exception(e)

    simu_end = datetime.now()
    simu_diff = simu_end - simu_start
    simu_seconds = simu_diff.total_seconds()
    print(f"{iterations} iterations took {simu_seconds} seconds \n(or {simu_seconds / 60} minutes) \n(or {simu_seconds / 60 / 60} hours)")
