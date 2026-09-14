import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from datetime import date, timedelta


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

@st.cache_data(ttl=900)
def download_stock_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    Results are cached for 15 minutes.
    """

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        return df

    # Handle MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df


def create_price_chart(df, ticker):
    """Create closing-price chart."""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Closing Price"
        )
    )

    fig.update_layout(
        title=f"{ticker} Closing Price",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def create_moving_average_chart(df, ticker):
    """Create closing-price and moving-average chart."""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA20"],
            mode="lines",
            name="MA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA50"],
            mode="lines",
            name="MA50"
        )
    )

    fig.update_layout(
        title=f"{ticker} Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def create_daily_returns_chart(df, ticker):
    """Create daily returns chart."""

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Returns(%)"],
            name="Daily Returns"
        )
    )

    fig.update_layout(
        title=f"{ticker} Daily Returns",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


def create_monthly_returns_chart(df_monthly, ticker):
    """Create monthly returns chart."""

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_monthly.index,
            y=df_monthly["Monthly_Returns(%)"],
            name="Monthly Returns"
        )
    )

    fig.update_layout(
        title=f"{ticker} Monthly Returns",
        xaxis_title="Month",
        yaxis_title="Return (%)",
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📈 Stock Analysis Dashboard")

st.caption(
    "Explore historical prices, moving averages, daily returns, "
    "monthly returns, and basic risk statistics."
)


# --------------------------------------------------
# Sidebar inputs
# --------------------------------------------------

st.sidebar.header("Analysis Settings")

ticker = st.sidebar.text_input(
    "Stock ticker",
    value="AAPL",
    help="Examples: AAPL, MSFT, NVDA, TSLA, ^GSPC"
).upper().strip()

start_date = st.sidebar.date_input(
    "Start date",
    value=date.today() - timedelta(days=5 * 365)
)

end_date = st.sidebar.date_input(
    "End date",
    value=date.today()
)

run_analysis = st.sidebar.button(
    "Run Analysis",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Main analysis
# --------------------------------------------------

if run_analysis:

    # Validate ticker
    if not ticker:
        st.error("Please enter a stock ticker.")
        st.stop()

    # Validate dates
    if start_date >= end_date:
        st.error("The start date must be before the end date.")
        st.stop()

    with st.spinner(f"Downloading data for {ticker}..."):

        df = download_stock_data(
            ticker,
            start_date,
            end_date + timedelta(days=1)
        )

    # Validate downloaded data
    if df.empty:
        st.error(
            "No data was found. Check the ticker symbol and selected dates."
        )
        st.stop()

    if "Close" not in df.columns:
        st.error(
            "The downloaded data does not contain a closing-price column."
        )
        st.stop()

    # --------------------------------------------------
    # Calculations
    # --------------------------------------------------

    df = df[["Close"]].copy()

    df["Returns(%)"] = df["Close"].pct_change() * 100

    df["MA20"] = df["Close"].rolling(window=20).mean()

    df["MA50"] = df["Close"].rolling(window=50).mean()

    df["Previous_Close"] = df["Close"].shift(1)

    # Monthly data
    df_monthly = df[["Close"]].resample("ME").last()

    df_monthly["Monthly_Returns(%)"] = (
        df_monthly["Close"].pct_change() * 100
    )

    # --------------------------------------------------
    # Analysis values
    # --------------------------------------------------

    latest_close = df["Close"].iloc[-1]
    highest_close = df["Close"].max()
    lowest_close = df["Close"].min()

    average_daily_return = df["Returns(%)"].mean()
    daily_volatility = df["Returns(%)"].std()

    highest_date = df["Close"].idxmax()
    lowest_date = df["Close"].idxmin()

    valid_daily_returns = df["Returns(%)"].dropna()

    best_day = valid_daily_returns.idxmax()
    worst_day = valid_daily_returns.idxmin()

    valid_monthly_returns = (
        df_monthly["Monthly_Returns(%)"].dropna()
    )

    # --------------------------------------------------
    # Status message
    # --------------------------------------------------

    st.success(
        f"Showing {ticker} data from "
        f"{start_date} to {end_date}."
    )

    # --------------------------------------------------
    # Summary metrics
    # --------------------------------------------------

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    metric_col1.metric(
        "Latest Close",
        f"${latest_close:.2f}"
    )

    metric_col2.metric(
        "Highest Close",
        f"${highest_close:.2f}"
    )

    metric_col3.metric(
        "Average Daily Return",
        f"{average_daily_return:.2f}%"
    )

    metric_col4.metric(
        "Daily Volatility",
        f"{daily_volatility:.2f}%"
    )

    # --------------------------------------------------
    # Key observations
    # --------------------------------------------------

    st.subheader("Key Observations")

    observation_col1, observation_col2 = st.columns(2)

    with observation_col1:

        st.write(
            f"**Highest closing price:** "
            f"${df.loc[highest_date, 'Close']:.2f} "
            f"on {highest_date.strftime('%Y-%m-%d')}"
        )

        st.write(
            f"**Lowest closing price:** "
            f"${df.loc[lowest_date, 'Close']:.2f} "
            f"on {lowest_date.strftime('%Y-%m-%d')}"
        )

        st.write(
            f"**Best trading day:** "
            f"{df.loc[best_day, 'Returns(%)']:.2f}% "
            f"on {best_day.strftime('%Y-%m-%d')}"
        )

    with observation_col2:

        st.write(
            f"**Worst trading day:** "
            f"{df.loc[worst_day, 'Returns(%)']:.2f}% "
            f"on {worst_day.strftime('%Y-%m-%d')}"
        )

        if not valid_monthly_returns.empty:

            best_month = valid_monthly_returns.idxmax()
            worst_month = valid_monthly_returns.idxmin()

            st.write(
                f"**Best month:** "
                f"{df_monthly.loc[best_month, 'Monthly_Returns(%)']:.2f}% "
                f"in {best_month.strftime('%Y-%m')}"
            )

            st.write(
                f"**Worst month:** "
                f"{df_monthly.loc[worst_month, 'Monthly_Returns(%)']:.2f}% "
                f"in {worst_month.strftime('%Y-%m')}"
            )

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    overview_tab, price_tab, returns_tab, data_tab = st.tabs(
        [
            "Overview",
            "Prices",
            "Returns",
            "Raw Data"
        ]
    )

    # --------------------------------------------------
    # Overview tab
    # --------------------------------------------------

    with overview_tab:

        st.subheader("Closing Price")

        st.plotly_chart(
            create_price_chart(df, ticker),
            use_container_width=True,
            key="overview_price_chart"
        )

        st.subheader("Moving Averages")

        st.plotly_chart(
            create_moving_average_chart(df, ticker),
            use_container_width=True,
            key="overview_moving_average_chart"
        )

    # --------------------------------------------------
    # Prices tab
    # --------------------------------------------------

    with price_tab:

        st.subheader("Price and Moving-Average Analysis")

        st.plotly_chart(
            create_moving_average_chart(df, ticker),
            use_container_width=True,
            key="prices_moving_average_chart"
        )

        st.info(
            "MA20 represents the average closing price over the previous "
            "20 trading sessions. MA50 represents the average over the "
            "previous 50 trading sessions."
        )

    # --------------------------------------------------
    # Returns tab
    # --------------------------------------------------

    with returns_tab:

        st.subheader("Daily Returns")

        st.plotly_chart(
            create_daily_returns_chart(df, ticker),
            use_container_width=True,
            key="daily_returns_chart"
        )

        st.subheader("Monthly Returns")

        st.plotly_chart(
            create_monthly_returns_chart(df_monthly, ticker),
            use_container_width=True,
            key="monthly_returns_chart"
        )

        st.subheader("Return Statistics")

        return_statistics = df["Returns(%)"].agg(
            ["mean", "std", "min", "max"]
        ).to_frame("Value")

        return_statistics.index = [
            "Mean",
            "Standard Deviation",
            "Minimum",
            "Maximum"
        ]

        st.dataframe(
            return_statistics,
            use_container_width=True
        )

    # --------------------------------------------------
    # Raw data tab
    # --------------------------------------------------

    with data_tab:

        st.subheader("Daily Historical Data")

        st.dataframe(
            df.sort_index(ascending=False),
            use_container_width=True
        )

        st.subheader("Monthly Historical Data")

        st.dataframe(
            df_monthly.sort_index(ascending=False),
            use_container_width=True
        )

        csv_data = df.to_csv().encode("utf-8")

        st.download_button(
            label="Download Daily Data as CSV",
            data=csv_data,
            file_name=f"{ticker}_stock_analysis.csv",
            mime="text/csv"
        )

else:

    st.info(
        "Enter a ticker and select a date range in the sidebar, "
        "then click **Run Analysis**."
    )