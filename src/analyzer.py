import pandas as pd
import numpy as np


class StockAnalyzer:

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()


    # --------------------------------------------------
    # CLEAN DATA
    # --------------------------------------------------

    def clean_data(self) -> pd.DataFrame:

        self.data.dropna(inplace=True)

        return self.data


    # --------------------------------------------------
    # DAILY RETURN
    # --------------------------------------------------

    def calculate_daily_return(self) -> pd.DataFrame:

        self.data["Daily_Return"] = (
            self.data["Close"].pct_change() * 100
        )

        return self.data


    # --------------------------------------------------
    # MOVING AVERAGES
    # --------------------------------------------------

    def calculate_moving_averages(
        self,
        short_window: int = 20,
        long_window: int = 50
    ) -> pd.DataFrame:

        self.data["MA_20"] = (
            self.data["Close"]
            .rolling(window=short_window)
            .mean()
        )

        self.data["MA_50"] = (
            self.data["Close"]
            .rolling(window=long_window)
            .mean()
        )

        return self.data


    # --------------------------------------------------
    # RSI
    # --------------------------------------------------

    def calculate_rsi(
        self,
        period: int = 14
    ) -> pd.DataFrame:

        delta = self.data["Close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        average_gain = gain.rolling(
            window=period
        ).mean()

        average_loss = loss.rolling(
            window=period
        ).mean()

        rs = average_gain / average_loss

        self.data["RSI"] = 100 - (
            100 / (1 + rs)
        )

        return self.data


    # --------------------------------------------------
    # MACD
    # --------------------------------------------------

    def calculate_macd(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> pd.DataFrame:

        fast_ema = self.data["Close"].ewm(
            span=fast_period,
            adjust=False
        ).mean()

        slow_ema = self.data["Close"].ewm(
            span=slow_period,
            adjust=False
        ).mean()

        self.data["MACD"] = (
            fast_ema - slow_ema
        )

        self.data["MACD_Signal"] = (
            self.data["MACD"]
            .ewm(
                span=signal_period,
                adjust=False
            )
            .mean()
        )

        self.data["MACD_Histogram"] = (
            self.data["MACD"]
            - self.data["MACD_Signal"]
        )

        return self.data


    # --------------------------------------------------
    # VWAP
    # --------------------------------------------------

    def calculate_vwap(self) -> pd.DataFrame:

        typical_price = (
            self.data["High"]
            + self.data["Low"]
            + self.data["Close"]
        ) / 3

        cumulative_tpv = (
            typical_price
            * self.data["Volume"]
        ).cumsum()

        cumulative_volume = (
            self.data["Volume"]
        ).cumsum()

        self.data["VWAP"] = (
            cumulative_tpv
            / cumulative_volume
        )

        return self.data


    # --------------------------------------------------
    # VOLATILITY
    # --------------------------------------------------

    def calculate_volatility(self) -> float:

        returns = self.data[
            "Daily_Return"
        ].dropna()

        volatility = np.std(returns)

        return round(
            float(volatility),
            2
        )


    # --------------------------------------------------
    # PRICE CHANGE
    # --------------------------------------------------

    def calculate_price_change(self) -> float:

        first_price = self.data[
            "Close"
        ].iloc[0]

        latest_price = self.data[
            "Close"
        ].iloc[-1]

        change = (
            (latest_price - first_price)
            / first_price
        ) * 100

        return round(
            float(change),
            2
        )


    # --------------------------------------------------
    # 52 WEEK HIGH / LOW
    # --------------------------------------------------

    def get_52_week_high_low(self) -> dict:

        recent_data = self.data.tail(252)

        high_52 = recent_data[
            "High"
        ].max()

        low_52 = recent_data[
            "Low"
        ].min()

        return {
            "52 Week High": round(
                float(high_52),
                2
            ),

            "52 Week Low": round(
                float(low_52),
                2
            )
        }


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def get_summary(self) -> dict:

        close_prices = self.data["Close"]

        return {

            "Current Price": round(
                float(close_prices.iloc[-1]),
                2
            ),

            "Highest Price": round(
                float(
                    self.data["High"].max()
                ),
                2
            ),

            "Lowest Price": round(
                float(
                    self.data["Low"].min()
                ),
                2
            ),

            "Average Price": round(
                float(close_prices.mean()),
                2
            ),

            "Total Volume": int(
                self.data["Volume"].sum()
            )
        }