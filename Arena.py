from stable_baselines3 import PPO, A2C, DQN, HerReplayBuffer
from stable_baselines3.her.goal_selection_strategy import GoalSelectionStrategy
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

from TradingGameEnvPos import TradingGameEnv as TradingGameEnv_0
from TradingGameEnvPos2 import TradingGameEnv as TradingGameEnv_1
from TradingGameEnvPos3 import TradingGameEnv as TradingGameEnv_2
from TradingGameEnvPos4 import TradingGameEnv as TradingGameEnv_3

goal_selection_strategy = 'future'
online_sampling = True

class Arena:
  def __init__(self, rules=0, saveName='model-'):
    self.saveName = saveName
    if rules==0:
      TradingGameEnv = TradingGameEnv_0
    elif rules==1:
      TradingGameEnv = TradingGameEnv_1
    elif rules==2:
      TradingGameEnv = TradingGameEnv_2
    elif rules==3:
      TradingGameEnv = TradingGameEnv_3
    self.env0 = TradingGameEnv()
    self.env = make_vec_env(lambda: self.env0, n_envs=1)
    self.model = DQN('MlpPolicy', self.env, verbose=1)
  
  def getSaveCallback(self):
    return CheckpointCallback(
      save_freq=1000,
      save_path="./models/",
      name_prefix=self.saveName+'_'
    )

  def save(self, name):
    self.model.save(name)
  
  def load(self, name):
    self.model = DQN.load(name, env=self.env)

  def train(self, timesteps=5000):
    self.model.learn(timesteps, callback=self.getSaveCallback())

  def actionStr(self, action):
    if action[0]==0:
        return 'WAIT'
    elif action[0]==1:
        return 'BUY'
    elif action[0]==2:
        return 'SELL'

  def testEnv(self):
    actions = {'5':1, '9':2, '12': 2, '20':1, '21':1, '25':1,'30':2, '40': 1, '41':2, '42': 1, '43': 1, '65': 1}
    obs = self.env.reset()
    for step in range(0,150):
      action = [0]
      if str(step) in actions:
        action = [actions[str(step)]]
      obs, reward, done, info = self.env.step(action)
      #print("Step {}\t{}\t{: .6f}\t{}".format(step + 1, self.actionStr(action), reward[0], list(obs[0][-6:])))

  def test(self):
    # Test the trained agent
    obs = self.env.reset()
    n_steps = 200000
    for step in range(n_steps):
      (action, _) = self.model.predict(obs, deterministic=True)
      obs, reward, done, info = self.env.step(action)
      #print("Step {}\t{}\t{: .3f}\t{}".format(step + 1, self.actionStr(action), reward[0], list(obs[0][-3:])))
      self.env.render(mode='console')
      print("Step {}\t{}\t{}".format(step + 1, self.actionStr(action), reward))
      if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        print("Goal reached!", "reward=", reward)
        break
