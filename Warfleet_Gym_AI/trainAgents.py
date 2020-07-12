import gym
import gym_wf
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import TRPO
from stable_baselines import PPO2, A2C
import os, os.path

from mlp import Policy


def main():
    # choose the algorithm which should be trained
    alg_input = input("Select algorithm (PPO2 or A2C only): ")
    timesteps_input = int(input("Choose number of timesteps: "))
    model_save = "trained_agents\\" + input("Select model to test(input filename, eg. a2c_wf_2 or ppo2_wf_4):")

    # the enviroment is generated
    env = gym.make("WARFLEET-v0")
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: env])
    log_dir = "./logs/"

    # start training by input
    if alg_input == "A2C" or alg_input == "a2c":
        model = A2C(MlpPolicy, env, verbose=1, tensorboard_log=log_dir)
        model.learn(total_timesteps=timesteps_input)
        model.save(model_save)
    else:
        if alg_input == "PPO2" or alg_input == "ppo2":
            model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log=log_dir, cliprange=0.1, gamma=0.99, ent_coef=0.001, vf_coef=0.2)
            model.learn(total_timesteps=timesteps_input)
            model.save(model_save)
        else:
            print("incorrect input")



if __name__ == "__main__":
    main()