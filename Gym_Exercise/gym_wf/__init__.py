from gym.envs.registration import register

register(
    id="WARFLEET-v0",
    entry_point="gym_wf.envs:CustomEnv",
    max_episode_steps = 1000,
)
