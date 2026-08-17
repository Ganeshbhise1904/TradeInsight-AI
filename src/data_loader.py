import yfinance as yf
import pandas as pd


class DataLoader:
    def __init__(self, symbol: str, period: str = "6mo"):
        self.symbol = symbol.upper()
        self.period = period

    def fetch_data(self) -> pd.DataFrame:
        try:
            stock = yf.Ticker(self.symbol)
            data = stock.history(period=self.period)

            if data.empty:
                raise ValueError(
                    f"No data found for symbol: {self.symbol}"
                )

            data.reset_index(inplace=True)

            return data

        except Exception as e:
            raise RuntimeError(
                f"Error while fetching stock data: {e}"
            )