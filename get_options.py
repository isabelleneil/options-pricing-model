import yfinance as yf
from datetime import datetime


def get_option_data(ticker, min_days):
    """Pull the option chain and stock price for the first expiry at least min_days away."""
    stock = yf.Ticker(ticker)

    # pick the first expiry at least min_days away
    today = datetime.today()
    expiry = None
    for date_str in stock.options:
        days_left = (datetime.strptime(date_str, "%Y-%m-%d") - today).days
        if days_left >= min_days:
            expiry = date_str
            break

    if expiry is None:
        raise ValueError(f"No expiry at least {min_days} days out for {ticker}")

    # option_chain returns two tables: calls and puts
    chain = stock.option_chain(expiry)
    calls = chain.calls
    puts = chain.puts

    # most recent closing price of the stock
    stock_price = stock.history(period="1d")["Close"].iloc[-1]

    return calls, puts, stock_price, expiry


if __name__ == "__main__":
    calls, puts, stock_price, expiry = get_option_data("AAPL", 30)
    print("Expiry:", expiry)
    print("Stock price:", round(stock_price, 2))
    print(calls[["strike", "bid", "ask", "lastPrice"]].head(10))