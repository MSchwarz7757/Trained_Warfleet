from gym.envs.registration import register

register(
    id="TTT-v0",
    entry_point="gym_ttt.envs:CustomEnv",
    max_episode_steps=5,
)
