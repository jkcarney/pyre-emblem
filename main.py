import environment
import unit_populator


def main():
    n = 100  # iterations
    env = environment.Environment()

    for _ in range(n):
        env.reset()
        blue_team = unit_populator.generate_blue_team(env.map)
        red_team = unit_populator.generate_red_team(env.map, blue_team)

        done = False

        while not done:
            for agent in blue_team:
                state = env.obtain_state(agent, blue_team, red_team)
                action = agent.determine_action(state, env, blue_team, red_team)
                move = agent.determine_move(action, blue_team, red_team, env)

                next_state, reward, done, info = env.step(agent, move, action, blue_team, red_team)

                agent.update_qtable(state, reward, action)

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

            print('== RED PHASE ==')
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
        map(lambda u: u.close(), blue_team)


if __name__ == "__main__":
    main()
