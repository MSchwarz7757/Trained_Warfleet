import gym
import gym_wf
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import TRPO
from stable_baselines import PPO2, A2C

from mlp import Policy

#from Warfleet_Gym_AI.gym_wf.envs import wf_env as e


def main():
    alg_input = input("Select algorithm (PPO2 or A2C only):")
    if alg_input != "PPO2" and alg_input != "A2C":
        print("Not an option (PPO2 or A2C only) !")
        alg_input = input("Select algorithm (PPO2 or A2C only):")
    model_input = "trained_agents\\" + input("Select model to test(input filename, eg. a2c_wf_2):")

    env = gym.make("WARFLEET-v0")
    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: env])
    log_dir = "./logs/"

    done = False
    stage_reward = 0
    turns = 0

    if alg_input == "PPO2":
        model = PPO2.load(model_input, env=env, tensorboard_log=log_dir)
    elif alg_input == "A2C":
        model = A2C.load(model_input, env=env, tensorboard_log=log_dir)

    obs = env.reset()

    while not done:
        # print("Game is running")
        action, _states = model.predict(obs)
        # print("---------------action:", action.shape, action)
        obs, reward, done, info = env.step(action)
        stage_reward += reward
        turns = turns + 1
        # print("Reward in ever round: {}".format(reward))
        # env.render()
        # print("Trefferliste: {}".format(env.hitlist_agent))

    print("Reward: {} /42".format(stage_reward))
    print("Turns: {}".format(turns))

    # insert into steps function in wf_env
    # print("Remaining Ships Computer: {}".format(len(self.shiplist_enemy)))
    # print("Remaining Ships Agent: {}".format(len(self.shiplist_agent)))

    env.close()


if __name__ == "__main__":
    main()
