# Evaluating Trading Strategies Using Python

The following basic trading strategies are implemented and evaluated as part of this analysis:

* Bollinger Bands
* Simple Moving Average Cross Over
* Buy and Hold

We start by [analysing](notebooks/Market-Data-EDA.ipynb) the [dataset downloaded from Kaggle]([1]) that contains stock and ETF OHLC (Open, High, Low, Close) prices. This dataset consists of a large number of individual files with each containing market data for one ticker. We first develop a market data API that abstracts away access to ticker files before proceeding with an EDA.

We then implement a simple backtester for running trading strategies. As part of it we develop a number of Python classes: Strategy, Backtest, ConfigSearch, etc. The backtester allows us to search for the best perforing ticker & strategy combinations. We run a backtest for all 3 strategies using 5 year's worth of market data.

Run containing usage examples:

### Getting Started

Install prerequisites:
```
$ conda env create -f environment.yml 
```
Jupyter notebooks are located under ```notebooks``` directory.

### Potential Future Improvements

* Implement and evaluate the Pair T
* Develop a more sophisticated backtester
  - Extend the current backtester to support multiple tickers

### References

* Kaggle dataset:
  * https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

[1]: https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs
