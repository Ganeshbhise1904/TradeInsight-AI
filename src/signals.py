import pandas as pd


class TradingSignal:

    def __init__(
        self,
        data: pd.DataFrame
    ):
        self.data = data


    # --------------------------------------------------
    # INDIVIDUAL SIGNALS
    # --------------------------------------------------

    def get_indicator_signals(self):

        if len(self.data) < 50:

            return {
                "MA": "Not Enough Data",
                "RSI": "Not Enough Data",
                "MACD": "Not Enough Data",
                "VWAP": "Not Enough Data"
            }


        latest = self.data.iloc[-1]

        signals = {}


        # MOVING AVERAGE

        if latest["MA_20"] > latest["MA_50"]:

            signals["MA"] = "Bullish"

        else:

            signals["MA"] = "Bearish"


        # RSI

        if latest["RSI"] < 30:

            signals["RSI"] = "Bullish"

        elif latest["RSI"] > 70:

            signals["RSI"] = "Bearish"

        else:

            signals["RSI"] = "Neutral"


        # MACD

        if latest["MACD"] > latest["MACD_Signal"]:

            signals["MACD"] = "Bullish"

        elif latest["MACD"] < latest["MACD_Signal"]:

            signals["MACD"] = "Bearish"

        else:

            signals["MACD"] = "Neutral"


        # VWAP

        if latest["Close"] > latest["VWAP"]:

            signals["VWAP"] = "Bullish"

        elif latest["Close"] < latest["VWAP"]:

            signals["VWAP"] = "Bearish"

        else:

            signals["VWAP"] = "Neutral"


        return signals


    # --------------------------------------------------
    # SIGNAL SCORE
    # --------------------------------------------------

    def calculate_score(self):

        signals = self.get_indicator_signals()

        score = 0

        for value in signals.values():

            if value == "Bullish":

                score += 1

            elif value == "Bearish":

                score -= 1


        return score


    # --------------------------------------------------
    # FINAL SIGNAL
    # --------------------------------------------------

    def generate_signal(self):

        if len(self.data) < 50:

            return "Not Enough Data"


        score = self.calculate_score()


        if score >= 3:

            return "STRONG BUY"

        elif score >= 1:

            return "BUY"

        elif score == 0:

            return "HOLD"

        elif score <= -3:

            return "STRONG SELL"

        else:

            return "SELL"