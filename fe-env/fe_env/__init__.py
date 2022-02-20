from gym.envs.registration import register

register(
    id='fe-env-v0',
    entry_point='fe_env.envs:FireEmblemEnvironment'
)
