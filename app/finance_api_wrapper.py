from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf

class FinanceAPIWrapper(ABC):
    @abstractmethod
    def get_stock_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass

class YahooFinanceAPIWrapper(FinanceAPIWrapper):
    def get_stock_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data[['Open', 'High', 'Low', 'Close', 'Volume']]