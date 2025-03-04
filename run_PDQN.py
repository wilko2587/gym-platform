from PDQN3 import PDQNAgent, play
import gym
import gym_platform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

if __name__=='__main__':
    env = gym.make("Platform-v0")

    # Network/setup params
    actorNet_kwargs = {'hidden_layers': (256, 256), 'l2': 1e-6, 'lr': 1e-3}
    paramNet_kwargs = {'hidden_layers': (256, 256), 'l2': 1e-6, 'lr': 1e-4}
    Nepisodes = 20000

    # initialise PDQN agent
    agent = PDQNAgent(observation_space=env.observation_space,
                          action_space=env.action_space,
                          actorNet_kwargs=actorNet_kwargs,
                          paramNet_kwargs=paramNet_kwargs,
                          train_start=500,
                          epsilon_decay=0.995,
                          epsilon_min=0.1,
                          epsilon_bumps=[], # can reset epsilon to init value when it hits values inside this list
                          epsilon_grad=0,#0.25,
                          memory_size=10000,
                          batch_size=128,
                          pct_thresh=0.5, # percentile threshold of prior 100 scores at which to start boosting epsilon
                          gamma=0.9,
                          grad_clipping=10.,
                          actor_softness=0.1,
                          param_softness=0.001,
                          stratify_replay_memory=False)

    #agent.load(id=1)
    # train agent, and get scores for each episode
    scores = play(env, agent, episodes=Nepisodes, render=False, train=True)

    #agent.save(id=1)

    # ----- Plotting -----
    # bin the episodes into 500 length bins
    scores_binned = pd.DataFrame(index=np.floor(np.arange(0, len(scores)) / 500.) * 500, columns=['score'], data=scores)
    scores_binned = scores_binned.reset_index()
    scores_binned = scores_binned.rename(columns={'index': 'episode'})
    f = plt.figure()
    sns.pointplot(data=scores_binned, y='score', x='episode', errwidth=0.5, linewidth=0.5)

    # save results
    plt.savefig('result.png')
    scores_binned.to_csv('results.csv')
