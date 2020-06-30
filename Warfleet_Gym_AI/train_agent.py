from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy
import numpy as np
from mlp import Policy
import gym
import gym_wf

def main():
    # env = gym.make("CartPole-v1")
    env = gym.make("WARFLEET-v0")
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: env])
    log_dir = "./logs/"
    model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log=log_dir, cliprange=0.02, n_steps=500, nminibatches=4)

    time_steps = int(input("How many timesteps to train the agent: "))
    model.learn(total_timesteps=time_steps)

    # just to seperate lerning phase and game phase
    num_episodes = int(input("How many games should the agent play: "))
    #model.save("warfleet")

    done = False
    #model = PPO2.load("warfleet")
    all_episode_rewards = []

    for i in range(num_episodes):
        print("--- New Game has started ---")
        obs = env.reset()
        episode_rewards = []
        done = False
        while not done:
            print("--- Game is running ---")
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            episode_rewards.append(reward)
            env.render()
        env.close()
        all_episode_rewards.append(sum(episode_rewards))

    mean_episode_reward = np.mean(all_episode_rewards)
    print("Mean reward:", mean_episode_reward, "Num episodes:", num_episodes)

if __name__ == "__main__":
    main()