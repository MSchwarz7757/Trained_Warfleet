# Trained Warfleet
This project is part of our participation in the *intelligent systems* course at the [HSD]( https://hs-duesseldorf.de/) in Düsseldorf, Germany.   
The goal is the implementation and training of an agent, capable of competently playing the board game "warfleet", in python using reinforcement learning.     
To achieve this we also had to develop a feasible environment for the agent to be trained in.   
For this purpose we chose the [OpenAI Gym](https://gym.openai.com/) toolkit, which provides an easy-to-use suite of reinforcement learning
tasks.

## Current State:
Right now the *environment* should be ready to be used to train *agents*.
The rules of the game and the process of playing have been implemented. 
Currently a basic *agent*, which takes random actions, is set up to play against a simple *AI*, which in turn also takes random actions. 
The agent gains a *small reward* for every hit and a *greater reward* for winning a match.

(desc spaces)

## Usage Instructions:

## Future Outlook:
Next up is the incorporation of reinforcement learning algorithems using the [Baselines](https://github.com/openai/baselines) framwork leading into the training of multiple agents with different algorithems.

