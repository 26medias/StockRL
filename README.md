# StockRL

Learning to play a trading game buy learning sets of rules

## Training Rules

1. Learn the basic rules of trading: `1M timesteps`
   - One position at a time.
   - Can't sell if you don't have a position open.
   - Can't buy again if you already have a position.
2. Learn not to hold the positions open too long: `1M timesteps`
   - After training on Rule #1 on 20 years of data, it learns to buy & hold for years, so we slowly drops the rewards to zero after 20 days of holding a position open.
3. Learn the basics of position management: `50M timesteps`
   - Close losing positions
   - Keep winning positions open longer for a larger reward
   - Close the position when the gains drop from previous steps (2, 5 & 10 days change)
4. Learn to detect trading opportunities before buying: `50M timesteps`
   - After Rule #3, the money management is pretty good, but a lot of positions are opened then immediately closed in downtrends

## Training

    python train.py

## Testing

    python test.py

## Data

20 years of cleaned-up daily data from Yahoo Finance on 491 stocks, saved in Pandas Pickle format.

## Features

Data shape: `(146, )`

- Candle [last 20]
- Volume [last 20]
- OBV [last 20]
- OBVdelta [last 20]
- Donchian [last 20]
- Trend [last 20]
- TrendDelta [last 20]
- 1 if a position is open, 0 otherwise
- Position gains if a position is open, 0 otherwise
- PositionAge/100 if a position is open, 0 otherwise
- getChange(2) if a position is open, 0 otherwise
- getChange(5) if a position is open, 0 otherwise
- getChange(10) if a position is open, 0 otherwise

Note: getChange(x) returns posValue[-1]-posValue[-x]/posValue[-x]

## Files

- Datacache.py
  - Download the datasets from Yahoo Finance in pandas pkl format
- Datacheck.py
  - Cleanup the dataset files (remove 0 values)
  - Display each dataset's stats via pandas describe()
- Datafeed.py
  - Read a dataset file
  - Calculate the relevant technical indicators used
    - OBV
    - OBV Delta
    - Downchian Chanels (relative position of the price within)
    - 200 SMA Trend (relative position of the price)
    - Trend Delta
- TradingGame.py
  - The Trading Game the AI will learn to play
  - Expose various actions:
    - Step
    - Buy
    - Sell
  - Expose various stats used in reward calculations
  - Returns the `(146, )` numpy context
  - Logs & chart the results
- TradingGameEnv[n].py
  - The Custom Env, each one teaching a different aspect of the game
- Arena.py
  - Trains & tests models on the various rules
  - Load models
  - Save models
  - Train
    - Checkpoints are saved at a 1M timestep interval
  - Test
  - Test the env validity
- train.py
  - Train a new model on the various rules, one after the other
- test.py
  - Test a model