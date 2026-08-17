import streamlit as st

from src.data_loader import DataLoader
from src.analyzer import StockAnalyzer
from src.signals import TradingSignal


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TradeInsight AI",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 TradeInsight AI")

st.subheader(
    "Stock Market Analysis & Trading Signal Dashboard"
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ Stock Settings")


symbol = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
)

period = st.sidebar.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y"
    ]
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.sidebar.button("🚀 Analyze Stock"):

    if not symbol.strip():

        st.warning(
            "Please enter a valid stock symbol."
        )

    else:

        try:

            with st.spinner(
                "Fetching stock data and analyzing..."
            ):

                # ------------------------------------------
                # LOAD DATA
                # ------------------------------------------

                loader = DataLoader(
                    symbol.upper(),
                    period
                )

                data = loader.fetch_data()


                # ------------------------------------------
                # VALIDATE DATA
                # ------------------------------------------

                if data is None or data.empty:

                    st.error(
                        "No data found. Please enter a valid stock symbol."
                    )

                    st.stop()


                # ------------------------------------------
                # ANALYZER
                # ------------------------------------------

                analyzer = StockAnalyzer(data)

                analyzer.clean_data()

                analyzer.calculate_daily_return()

                analyzer.calculate_moving_averages()

                analyzer.calculate_rsi()

                analyzer.calculate_macd()

                analyzer.calculate_vwap()


                processed_data = analyzer.data


                # ------------------------------------------
                # TRADING SIGNAL
                # ------------------------------------------

                signal_generator = TradingSignal(
                    processed_data
                )

                signal = (
                    signal_generator.generate_signal()
                )

                indicator_signals = (
                    signal_generator.get_indicator_signals()
                )

                signal_score = (
                    signal_generator.calculate_score()
                )


                # ------------------------------------------
                # SUMMARY
                # ------------------------------------------

                summary = analyzer.get_summary()

                price_change = (
                    analyzer.calculate_price_change()
                )

                high_low = (
                    analyzer.get_52_week_high_low()
                )


            # ----------------------------------------------
            # SUCCESS MESSAGE
            # ----------------------------------------------

            st.success(
                f"Analysis completed for {symbol.upper()}"
            )


            # ----------------------------------------------
            # STOCK INFORMATION
            # ----------------------------------------------

            st.subheader(
                "🏢 Stock Information"
            )

            info_col1, info_col2 = st.columns(2)

            info_col1.write(
                f"**Stock Symbol:** {symbol.upper()}"
            )

            info_col2.write(
                f"**Analysis Period:** {period}"
            )


            # ----------------------------------------------
            # MAIN METRICS
            # ----------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Current Price",
                f"${summary['Current Price']}"
            )

            col2.metric(
                "Highest Price",
                f"${summary['Highest Price']}"
            )

            col3.metric(
                "Lowest Price",
                f"${summary['Lowest Price']}"
            )

            col4.metric(
                "Volatility",
                f"{analyzer.calculate_volatility()}%"
            )


            # ----------------------------------------------
            # PRICE PERFORMANCE
            # ----------------------------------------------

            st.subheader(
                "📈 Price Performance"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Price Change",
                f"{price_change}%"
            )

            col2.metric(
                "52 Week High",
                f"${high_low['52 Week High']}"
            )

            col3.metric(
                "52 Week Low",
                f"${high_low['52 Week Low']}"
            )


            st.divider()


            # ----------------------------------------------
            # FINAL TRADING SIGNAL
            # ----------------------------------------------

            st.subheader(
                "📊 Final Trading Signal"
            )


            if signal == "STRONG BUY":

                st.success(
                    "🚀🟢 STRONG BUY SIGNAL"
                )

            elif signal == "BUY":

                st.success(
                    "🟢 BUY SIGNAL"
                )

            elif signal == "HOLD":

                st.warning(
                    "🟡 HOLD SIGNAL"
                )

            elif signal == "SELL":

                st.error(
                    "🔴 SELL SIGNAL"
                )

            elif signal == "STRONG SELL":

                st.error(
                    "🚨🔴 STRONG SELL SIGNAL"
                )

            else:

                st.info(
                    "⚪ Not Enough Data"
                )


            # ----------------------------------------------
            # SIGNAL SCORE DASHBOARD
            # ----------------------------------------------

            st.subheader(
                "🎯 Signal Score Dashboard"
            )

            score_col1, score_col2, score_col3, score_col4 = (
                st.columns(4)
            )


            score_col1.metric(
                "MA Signal",
                indicator_signals["MA"]
            )

            score_col2.metric(
                "RSI Signal",
                indicator_signals["RSI"]
            )

            score_col3.metric(
                "MACD Signal",
                indicator_signals["MACD"]
            )

            score_col4.metric(
                "VWAP Signal",
                indicator_signals["VWAP"]
            )


            st.metric(
                "Overall Signal Score",
                signal_score
            )


            st.divider()


            # ----------------------------------------------
            # PRICE + MOVING AVERAGE CHART
            # ----------------------------------------------

            st.subheader(
                "📈 Closing Price & Moving Averages"
            )

            chart_data = (
                processed_data
                .set_index("Date")[
                    [
                        "Close",
                        "MA_20",
                        "MA_50"
                    ]
                ]
            )

            st.line_chart(
                chart_data,
                use_container_width=True
            )


            # ----------------------------------------------
            # PRICE RANGE / CANDLE DATA
            # ----------------------------------------------

            st.subheader(
                "🕯️ Price Range Analysis"
            )

            price_range_data = (
                processed_data
                .set_index("Date")[
                    [
                        "Open",
                        "High",
                        "Low",
                        "Close"
                    ]
                ]
            )

            st.line_chart(
                price_range_data,
                use_container_width=True
            )


            # ----------------------------------------------
            # VOLUME
            # ----------------------------------------------

            st.subheader(
                "📊 Trading Volume"
            )

            volume_data = (
                processed_data
                .set_index("Date")[
                    ["Volume"]
                ]
            )

            st.bar_chart(
                volume_data,
                use_container_width=True
            )


            # ----------------------------------------------
            # RSI
            # ----------------------------------------------

            st.subheader(
                "📊 RSI Analysis"
            )

            rsi_data = (
                processed_data
                .set_index("Date")[
                    ["RSI"]
                ]
            )

            st.line_chart(
                rsi_data,
                use_container_width=True
            )

            latest_rsi = (
                processed_data["RSI"]
                .iloc[-1]
            )

            if latest_rsi > 70:

                st.warning(
                    f"RSI: {latest_rsi:.2f} "
                    "— Overbought Zone ⚠️"
                )

            elif latest_rsi < 30:

                st.success(
                    f"RSI: {latest_rsi:.2f} "
                    "— Oversold Zone 🟢"
                )

            else:

                st.info(
                    f"RSI: {latest_rsi:.2f} "
                    "— Neutral Zone"
                )


            # ----------------------------------------------
            # MACD
            # ----------------------------------------------

            st.subheader(
                "📉 MACD Analysis"
            )

            macd_data = (
                processed_data
                .set_index("Date")[
                    [
                        "MACD",
                        "MACD_Signal",
                        "MACD_Histogram"
                    ]
                ]
            )

            st.line_chart(
                macd_data,
                use_container_width=True
            )

            latest_macd = (
                processed_data["MACD"]
                .iloc[-1]
            )

            latest_macd_signal = (
                processed_data["MACD_Signal"]
                .iloc[-1]
            )

            if latest_macd > latest_macd_signal:

                st.success(
                    f"MACD: {latest_macd:.2f} "
                    "— Bullish Momentum 🟢"
                )

            elif latest_macd < latest_macd_signal:

                st.warning(
                    f"MACD: {latest_macd:.2f} "
                    "— Bearish Momentum 🔴"
                )

            else:

                st.info(
                    "MACD and Signal Line are equal."
                )


            # ----------------------------------------------
            # VWAP
            # ----------------------------------------------

            st.subheader(
                "📊 VWAP Analysis"
            )

            vwap_data = (
                processed_data
                .set_index("Date")[
                    [
                        "Close",
                        "VWAP"
                    ]
                ]
            )

            st.line_chart(
                vwap_data,
                use_container_width=True
            )

            latest_close = (
                processed_data["Close"]
                .iloc[-1]
            )

            latest_vwap = (
                processed_data["VWAP"]
                .iloc[-1]
            )

            if latest_close > latest_vwap:

                st.success(
                    f"Price: ${latest_close:.2f} "
                    f"is above VWAP "
                    f"${latest_vwap:.2f} "
                    "— Bullish 🟢"
                )

            elif latest_close < latest_vwap:

                st.warning(
                    f"Price: ${latest_close:.2f} "
                    f"is below VWAP "
                    f"${latest_vwap:.2f} "
                    "— Bearish 🔴"
                )

            else:

                st.info(
                    "Current Price is equal to VWAP."
                )


            # ----------------------------------------------
            # SIGNAL EXPLANATION
            # ----------------------------------------------

            signal_explanation = {

                "STRONG BUY":
                    "Multiple indicators are showing strong bullish momentum.",

                "BUY":
                    "More indicators are bullish than bearish.",

                "HOLD":
                    "Indicators are showing mixed market conditions.",

                "SELL":
                    "More indicators are bearish than bullish.",

                "STRONG SELL":
                    "Multiple indicators are showing strong bearish momentum.",

                "Not Enough Data":
                    "More historical data is required for analysis."
            }


            st.subheader(
                "💡 Signal Explanation"
            )

            explanation = (
                signal_explanation.get(
                    signal,
                    "No explanation available."
                )
            )

            st.write(
                explanation
            )


            # ----------------------------------------------
            # DAILY RETURN
            # ----------------------------------------------

            st.subheader(
                "📉 Daily Return Analysis"
            )

            daily_return_data = (
                processed_data
                .set_index("Date")[
                    ["Daily_Return"]
                ]
            )

            st.line_chart(
                daily_return_data,
                use_container_width=True
            )


            # ----------------------------------------------
            # ADDITIONAL INSIGHTS
            # ----------------------------------------------

            st.subheader(
                "📊 Additional Insights"
            )

            positive_days = (
                processed_data[
                    "Daily_Return"
                ] > 0
            ).sum()

            negative_days = (
                processed_data[
                    "Daily_Return"
                ] < 0
            ).sum()


            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(
                "Average Price",
                f"${summary['Average Price']}"
            )

            col2.metric(
                "Total Trading Volume",
                f"{summary['Total Volume']:,}"
            )

            col3.metric(
                "Positive Trading Days",
                int(positive_days)
            )

            col4.metric(
                "Negative Trading Days",
                int(negative_days)
            )


            # ----------------------------------------------
            # MARKET PERFORMANCE
            # ----------------------------------------------

            st.subheader(
                "📌 Market Performance Summary"
            )

            latest_return = (
                processed_data[
                    "Daily_Return"
                ].iloc[-1]
            )


            if latest_return > 0:

                st.success(
                    f"Latest trading return is "
                    f"{latest_return:.2f}% "
                    "— Positive Performance 📈"
                )

            elif latest_return < 0:

                st.warning(
                    f"Latest trading return is "
                    f"{latest_return:.2f}% "
                    "— Negative Performance 📉"
                )

            else:

                st.info(
                    "No price change in the latest trading session."
                )


            # ----------------------------------------------
            # PROCESSED DATA
            # ----------------------------------------------

            st.subheader(
                "📋 Processed Stock Data"
            )

            st.dataframe(
                processed_data,
                use_container_width=True
            )


            # ----------------------------------------------
            # DOWNLOAD DATA
            # ----------------------------------------------

            st.divider()

            st.subheader(
                "📥 Download Data"
            )

            csv = (
                processed_data
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="⬇️ Download Processed Stock Data",
                data=csv,
                file_name=(
                    f"{symbol.upper()}_stock_analysis.csv"
                ),
                mime="text/csv",
                key="download_stock_data"
            )


        except Exception as e:

            st.error(
                f"Error: {e}"
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "⚠️ Educational project only. "
    "This dashboard does not provide financial advice."
)