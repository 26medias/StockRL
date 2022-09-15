import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class TradingGame:
  def __init__(self, data, depth=20, symbol=""):
    self.symbol = symbol
    self.depth = depth
    self.data = data
    self.size = len(data)
    self.rows = self.size-depth
    self.profits = 0
    self.cursor = depth
    self.lastSell = depth # Or idx of past action
    self.lastBuy = depth # Or idx of past action
    self.positionIdx = False # Or idx bought
    self.position = False # Or value bought
    self.log_price = []
    self.log_profits = []
    self.log_gains = []
    self.log_sell = []
    self.posProfits = None
    self.histPosValue = np.array([])
  
  def getStepData(self):
    if self.cursor>=self.size:
      return np.zeros((146, ))
    historical = self.data.iloc[self.cursor-self.depth:self.cursor].copy()
    historical = historical.drop(['Open'], axis=1)
    flatten = np.clip(historical.T.to_numpy(), a_max=1, a_min=-1).astype(np.float32).flatten()
    if self.position>0:
      posAge = min(self.positionAge()/100, 1)
      flatten = np.append(flatten, [1, self.positionGains(), posAge, self.getChange(2), self.getChange(5), self.getChange(10)])
    else: 
      flatten = np.append(flatten, [0, 0, 0, 0, 0, 0])
    return np.array(flatten).astype(np.float32)

  def step(self):
    if self.cursor == self.size-2:
      self.sell()
    current = self.getCurrent()
    self.log_price.append(current['Open'])
    self.log_profits.append(self.profits)
    self.log_gains.append(self.positionGains())
    self.log_sell.append(self.posProfits)
    if self.position>0:
      self.histPosValue = np.append(self.histPosValue, [current['Open']])
    self.cursor = self.cursor + 1
    if self.cursor >= self.size:
      return False
    return True
  
  def getChange(self, n):
    if self.histPosValue.shape[0]==0:
      return 0
    r = self.histPosValue[-n:]
    return (r[-1]-r[0])/r[0]
  
  def getCurrent(self):
    return self.data.iloc[self.cursor]
  
  def canSell(self):
    return self.position>0
  
  def positionGains(self):
    if self.position>0:
      return (self.getCurrent()['Open']-self.position)/self.position
    return 0
  
  def positionProfits(self):
    if self.position>0:
      return (self.getCurrent()['Open']-self.position)
    return 0
  
  def positionAge(self):
    return self.cursor-self.positionIdx
  
  def lastBuyAge(self):
    return self.cursor-self.lastBuy
  
  def lastSellAge(self):
    return self.cursor-self.lastSell
  
  def buy(self):
    if self.canSell():
      return False
    self.position = self.getCurrent()['Open']
    self.positionIdx = self.cursor
    self.lastBuy = self.cursor
    return True
  
  def sell(self):
    if not self.canSell():
      return False
    posProfits = (self.getCurrent()['Open']-self.position)
    posGains = posProfits/self.position
    self.profits = self.profits + posProfits
    self.posProfits = posProfits
    self.position = 0
    self.positionIdx = False
    self.lastSell = self.cursor
    self.histPosValue = np.array([])
    return posGains

  def plot(self):
    df = pd.DataFrame()
    df['Open'] = self.log_price
    #df['Open0'] = self.log_price[0]
    df['Profits'] = self.log_profits
    df['PosValue'] = self.log_gains
    df['Sell'] = self.log_sell
    df['0'] = 0
    self.chart([
      {'title':'Price ('+self.symbol+')', 'cols':['Open'], 'df':df},
      {'title':'Pos Value', 'cols':['PosValue', '0'], 'df':df},
      {'title':'Sell Value', 'cols':['Sell', '0'], 'df':df},
      {'title':'Profits', 'cols':['Profits', '0'], 'df':df}
    ])
    print(df.head(200))
    print(df.tail(200))

  def chart(self, plots, figsize=(40,20)):
    fig, ax = plt.subplots(len(plots), 1, figsize=figsize)
    for n,plot in enumerate(plots):
      ax[n].set_title(plot['title'])
      for col in plot['cols']:
        ax[n].plot(plot['df'].index, plot['df'][col])
    plt.show()
