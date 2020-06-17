"""Provides an access layer to stored locally market data files

This format is utilized as part of the following Kaggle dataset:

    * https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs
"""

from datetime import datetime
import os

import pandas as pd


class EquityData:
    """
    Provides an access layer to market data files made available
    as part of the following Kaggle dataset:

        https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

    Each file contains market data for one ticker (either stock or ETF). Also, each filename
    has a specific naming convention: it consists of a ticker and a suffix (common to all files).

    Attributes:
        stock_dir (str): Directory location for stock files.
        etf_dir (str): Directory location for ETF files.
        file_suffix (str): A file suffix used by stock & ETF files.
    """

    def __init__(self, data_dir, stock_dir, etf_dir, file_suffix=".us.txt"):
        self.stock_dir = os.path.join(data_dir, stock_dir)
        self.etf_dir = os.path.join(data_dir, etf_dir)
        self.file_suffix = file_suffix

    @staticmethod
    def _get_tickers(dirname, file_suffix):
        """
        Creates a list of available tickers for a given directory.

        Only non-empty files are returned.

        Args:
            file_suffix (str): A file suffix used by each data file.

        Returns:
            (List[str]): A list of available tickers.
        """
        tickers = []
        for file in os.listdir(dirname):
            # This dataset includes empty files which we exclude here.
            if os.stat(os.path.join(dirname, file)).st_size > 0:
                tickers.append(file.replace(file_suffix, ""))

        return tickers

    def get_etf_tickers(self):
        """
        Returns a list of available ETF tickers.

        Returns:
            (List[str]): A sorted list of available ETF tickers.
        """
        return sorted(self._get_tickers(self.etf_dir, self.file_suffix))

    def get_stock_tickers(self):
        """
        Returns a list of available stock tickers.

        Returns:
            (List[str]): A sorted list of available stock tickers.
        """
        return sorted(self._get_tickers(self.stock_dir, self.file_suffix))

    def get_all_tickers(self):
        """
        Returns a list of available stock and ETF tickers.

        Returns:
            (List[str]): A sorted list of available stock and ETF tickers.
        """
        return sorted(self.get_etf_tickers() + self.get_stock_tickers())

    def get_csv_data(self, ticker, start_date=None, end_date=None):
        """
        Returns a list of available stock and ETF tickers.

        Args:
            ticker (str): A ticker name.
            start_date (str): A start date
            end_date (str): An end date

        Returns:
            (pd.DataFrame): Parsed market data for a given ticker.
        """
        ticker = ticker.lower()

        # Check ETFs first since the number of potential hits is much smaller.
        if ticker in self.get_etf_tickers():
            dirname = self.etf_dir
        else:
            dirname = self.stock_dir

        result = pd.DataFrame()
        csv = pd.read_csv(os.path.join(dirname, ticker + self.file_suffix))
        result = pd.DataFrame(
            {
                "date": csv["Date"],
                "ticker": ticker,
                "price": csv["Close"],
                "volume": csv["Volume"],
            }
        )
        result["date"] = (
            result["date"].map(lambda t: datetime.strptime(t, "%Y-%m-%d")).to_numpy()
        )

        if start_date is not None:
            result = result[result["date"] >= start_date]

        if end_date is not None:
            result = result[result["date"] <= end_date]

        result.index = result.date

        # Only including weekdays
        result["dayofweek"] = pd.DatetimeIndex(result.index).dayofweek
        result = result[(result.dayofweek != 5) & (result.dayofweek != 6)]

        return result
