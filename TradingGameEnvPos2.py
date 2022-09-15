import pandas as pd
import numpy as np
import random
from os import listdir
from os.path import isfile, join

import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C

from TradingGame import TradingGame
from DataFeed import Datafeed



class TradingGameEnv(gym.Env):
  """
  Custom Environment
  Teaches to not hold to long
  """
  
  metadata = {'render.modes': ['console']}
  
  WAIT = 0
  BUY  = 1
  SELL = 2

  def __init__(self, grid_size=10):
    super(TradingGameEnv, self).__init__()
    self.action_space = spaces.Discrete(3)
    self.observation_space = spaces.Box(low=-1, high=1, shape=(146, ), dtype=np.float32)

  def reset(self):
    onlyfiles = [f for f in listdir('./data') if isfile(join('./data', f))]
    symbol = random.choice(onlyfiles) # 'AAPL.pkl' #random.choice(onlyfiles)
    print("== "+symbol+" ==")
    self.feed = Datafeed(symbol)
    self.game = TradingGame(self.feed.data, symbol=symbol)
    return self.game.getStepData()

  def inc(self, n, s, v):
    return min(v, (n/s)*v)
    
  def dec(self, n, s, v):
    return max(0, (1-(n/s))*v)

  def step(self, action):
    reward = 0
    badAction = -0.1
    minWait = 5   # Min wait between sell & buy again
    maxWait = 20  # Max wait between sell & buy again
    waitBetweenBuys = 5
    maxHold = 20

    if action == self.BUY:
      # Buy
      buyResponse = self.game.buy()
      if buyResponse == False:
        reward = badAction
      else:
        reward = 0
    elif action == self.SELL:
      # Sell
      sellResponse = self.game.sell()
      if sellResponse == False:
        reward = badAction
      else:
        if sellResponse>0:
          reward = sellResponse
        else:
          reward = 0
    elif action == self.WAIT:
      # Wait
      reward = 0
    
    #reward = min(1, max(-1, reward))
    
    stepSuccess = self.game.step()
    return self.game.getStepData(), reward, bool(stepSuccess==False), {}

  def render(self, mode='console'):
    if mode != 'console':
      raise NotImplementedError()
    if self.game.cursor==self.game.size-1:
        print("Profits", self.game.profits)
        self.game.plot()

  def close(self):
    pass


# If the environment don't follow the interface, an error will be thrown
env = TradingGameEnv()
check_env(env, warn=True)

"""
var v = function(n, steps, penalty) {
    return ((n/steps))*penalty;
}
for (let i=0;i<=10;i++) {console.log(i, ':', v(i, 10, 0.5))}
"""