
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta

from os import path

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


class Datafeed:
  def __init__(self, symbol):
    self.symbol = symbol
    self.refresh()
    self.transform()
  
  def chart(self, plots, figsize=(40,20)):
    fig, ax = plt.subplots(len(plots), 1, figsize=figsize)
    for n,plot in enumerate(plots):
      ax[n].set_title(plot['title'])
      for col in plot['cols']:
        ax[n].plot(plot['df'].index, plot['df'][col])
    plt.show()
  
  def refresh(self):
    #df = pd.DataFrame()
    #df = df.ta.ticker(self.symbol)
    df = pd.read_pickle("./data/"+self.symbol)
    df.set_index(pd.DatetimeIndex(df.index), inplace=True)
    df.ta.log_return(cumulative=True, append=True)
    df.ta.percent_return(cumulative=True, append=True)
    df.ta.strategy(ta.Strategy(
        name="Layer1",
        ta=[
            {"kind": "obv"},
            {"kind": "sma", "length": 200},
            {"kind": "donchian", "lower_length": 20, "upper_length": 20},
            {"kind": "donchian", "close": "OBV", "lower_length": 20, "upper_length": 20, "prefix": "OBV"}
        ]
    ))
    df['0'] = 0
    self.df = df
  
  def transform(self):
    output = pd.DataFrame(index=self.df.index)
    output['Open'] = self.df['Open'].shift(-1)
    output['Candle'] = (self.df['Close']-self.df['Open'])/self.df['Open']
    output['Volume'] = self.df['Volume']/self.df['Volume'].rolling(20).max()
    output['OBV'] = self.df['OBV']/self.df['OBV'].rolling(20).max()
    output['OBVdelta'] = (output['OBV']-output['OBV'].shift())/output['OBV'].shift()
    output['Donchian'] = (self.df['Open']-self.df['DCL_20_20'])/(self.df['DCU_20_20']-self.df['DCL_20_20'])
    output['Trend'] = (self.df['Open']-self.df['SMA_200'])/self.df['SMA_200']
    output['TrendDelta'] = output['Trend']-output['Trend'].shift()
    output = output.dropna()
    self.data = output

"""
feed = Datafeed('AMC')
feed.chart([
  {'title':'Price', 'cols':['Open','Close', 'SMA_200', 'DCL_20_20', 'DCU_20_20'], 'df':feed.df},
  {'title':'Volume', 'cols':['Volume'], 'df':feed.df},
  {'title':'OBV', 'cols':['OBV', 'OBV_DCL_20_20', 'OBV_DCU_20_20'], 'df':feed.df},
  {'title':'Log Return', 'cols':['CUMLOGRET_1', '0'], 'df':feed.df}
])
feed.data.describe()
"""