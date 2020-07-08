import gym
import gym_wf
import numpy as np


def main():
    env = gym.make("WARFLEET-v0")
    done = False
    # reward of the whole episode
    episode_reward = 0
    n_steps = 0
    # get the initial state of the environment
    state = env.reset()
    while not done:
        action = env.agent_move()
        next_state, reward, done, info = env.step(action)
        episode_reward += reward
        state = next_state
        n_steps += 1
    # just an empty line
    print()
    print()
    print("**** Last state after the game is finished ****")
    for row in state:
        print(row)
    print(
        "episode_reward:", episode_reward,
        "\tn_steps:", n_steps)

if __name__ == "__main__":
    main()
