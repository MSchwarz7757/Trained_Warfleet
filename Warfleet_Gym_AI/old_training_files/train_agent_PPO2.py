import gym
import gym_wf
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2
from stable_baselines import PPO2

from mlp import Policy


def main():
    env = gym.make("WARFLEET-v0")
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: env])
    log_dir = "./logs/"
    model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log=log_dir, cliprange=0.1, gamma=0.99, ent_coef=0.001, vf_coef=0.2)

    #model.learn(total_timesteps=10000000)
    #model.save("PPO2_wf_2")

    done = False
    stage_reward = 0
    input("Training is finished, press to play a game: ")

    model = PPO2.load("trained_agents/PPO2_wf_2", env=env, tensorboard_log=log_dir)

    obs = env.reset()

    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        stage_reward += reward
        # env.render()
    env.close()


if __name__ == "__main__":
    main()