import numpy as np
import yfinance as yf
from datetime import datetime

def get_risk_free_rate():
    """13-week U.S. T-bill yield as a decimal (0.04 means 4%)."""
    irx = yf.Ticker("^IRX")
    # 5 days so it still works on weekends or holidays
    latest = irx.history(period="5d")["Close"].iloc[-1]
    return latest / 100

def get_time_to_expiry(expiry):
    """Years between today and the expiry date ('YYYY-MM-DD')"""
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
    days_left = (expiry_date - datetime.today()).days
    return days_left / 365

def get_historical_volatility(ticker, period="1y"):
    """Annualized volatility from one year of daily log returns."""
    prices = yf.Ticker(ticker).history(period=period)["Close"]
    log_returns = np.log(prices / prices.shift(1)).dropna()
    return log_returns.std() * np.sqrt(252)

if __name__ == "__main__":
    print("r:", round(get_risk_free_rate(), 4))
    print("sigma:", round(get_historical_volatility("AAPL"), 4))