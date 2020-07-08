import gym
import gym_wf
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import TRPO
from stable_baselines import PPO2, A2C

from mlp import Policy


def main():
    # env = gym.make("CartPole-v1")
    env = gym.make("WARFLEET-v0")
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: env])
    log_dir = "./logs/"
    # model = PPO2(Policy, env, verbose=1, tensorboard_log=log_dir, cliprange=0.05)
    model = A2C(MlpPolicy, env, verbose=1, tensorboard_log=log_dir)
    print(model.episode_reward)

    # model.learn(total_timesteps=10000000)
    # model.save("a2c_wf_3")
    print("model.episode_reward: {}".format(model.episode_reward))
    print("model.rewards_ph: {}".format(model.rewards_ph))

    done = False
    stage_reward = 0
    input("Training is finished, press to play a game")

    model = A2C.load("a2c_wf_2", env=env, tensorboard_log=log_dir)

    obs = env.reset()

    while not done:
        print("Game is running")
        action, _states = model.predict(obs)
        print("---------------action:", action.shape, action)
        obs, reward, done, info = env.step(action)
        stage_reward += reward
        print("Reward in ever round: {}".format(reward))
        # env.render()
        # print("Trefferliste: {}".format(env.hitlist_agent))

    print("Reward: {} von insgesamt 32 notwendigen schüssen".format(stage_reward))
    env.close()


if __name__ == "__main__":
    main()