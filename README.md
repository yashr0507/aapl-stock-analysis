# AAPL Stock Analysis

## Overview
This project analyzes historical stock data for Apple (AAPL) using Python, Pandas, Matplotlib, and yfinance.

The goal was to evaluate:
- daily returns
- monthly returns
- volatility (standard deviation)
- moving averages
- overall stock trends

---

## Dataset
Historical stock data was downloaded using yfinance.

Ticker used:
- AAPL

Time period:
- 31st December, 2020 to 31st December, 2025

---

## Methods Used
- Data cleaning
- `pct_change()` → daily/monthly returns
- `rolling()` → moving averages
- `shift()` → previous closing price
- `resample()` → monthly data conversion
- visualization using Matplotlib

---

## Key Metrics Analyzed
- Average daily return
- Daily volatility
- Best trading day
- Worst trading day
- Best month
- Worst month

---

## Visualizations
This project includes:
- stock price trend chart
- moving average chart
- returns chart

---

## Key Insights
- Apple's stock prices show a long-term rise in price from 2021-2026 with an average daily return of 0.0746% despite short-term fluctuations
- Apple's stock price peaked on 2nd December, 2025 at $285.92
- Apple's stock price was at its lowest on 8th March, 2021 at $113.33
- Apple saw its highest return on 9th April, 2025 with a 15.329% increase in stock price from the previous day
- Apple saw its lowest return on 3rd April, 2025 with a 9.246% decrease in stock price from the previous day
- The best trading month was July 2022, with a return of 18.863%
- The worst trading month was December 2022, with a return of -12.227%
- April saw a period of increased volatility with the worst trading day and best trading day across the span of 5 years occuring within the same week


---

## Tools Used
- Python
- Pandas
- Matplotlib
- yfinance
- Jupyter Notebook
