import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from black_scholes import BlackScholesModel
from get_options import get_option_data
from market_inputs import get_risk_free_rate, get_time_to_expiry, get_historical_volatility

def implied_vol(market_price, S, K, T, r, option_type="call",
                low=0.001, high=3.0, tol=1e-6, max_iter=100):
    """Find the volatility that makes Black-Scholes match the market price, using bisection."""

    def price_at(sigma):
        model = BlackScholesModel(S, K, T, r, sigma)
        if option_type == "call":
            return model.call_option_price()
        return model.put_option_price()

    # if the market price is outside what the model can produce, there's no answer
    if market_price < price_at(low) or market_price > price_at(high):
        return np.nan

    for _ in range(max_iter):
        mid = (low + high) / 2
        if price_at(mid) > market_price:
            high = mid   # model too expensive, so the volatility guess is too high
        else:
            low = mid    # model too cheap, so the volatility guess is too low
        if high - low < tol:
            break

    return (low + high) / 2


if __name__ == "__main__":
    TICKER = "AAPL"
    calls, puts, S, expiry = get_option_data(TICKER, 30)
    T = get_time_to_expiry(expiry)
    r = get_risk_free_rate()
    hist_vol = get_historical_volatility(TICKER)

    # out-of-the-money only: puts below the stock price, calls above it
    otm_puts = puts[(puts["strike"] < S) & (puts["strike"] > 0.85 * S)].copy()
    otm_calls = calls[(calls["strike"] >= S) & (calls["strike"] < 1.15 * S)].copy()

    for df, kind in [(otm_puts, "put"), (otm_calls, "call")]:
        df["market_mid"] = (df["bid"] + df["ask"]) / 2
        df["type"] = kind
        df["my_iv"] = [
            implied_vol(price, S, K, T, r, kind)
            for price, K in zip(df["market_mid"], df["strike"])
        ]

    # one curve across all strikes
    curve = pd.concat([otm_puts, otm_calls]).sort_values("strike")
    print(curve[["strike", "type", "market_mid", "my_iv", "impliedVolatility"]].round(4))

    plt.plot(curve["strike"], curve["my_iv"], marker="o", label="Implied volatility (OTM options)")
    plt.axhline(hist_vol, linestyle="--", label=f"Historical volatility ({hist_vol:.1%})")
    plt.axvline(S, color="grey", linestyle=":", label=f"Stock price ({S:.0f})")
    plt.xlabel("Strike")
    plt.ylabel("Volatility")
    plt.title(f"{TICKER} implied volatility skew, expiry {expiry}")
    plt.legend()
    plt.savefig("volatility_smile.png", dpi=150, bbox_inches="tight")
    plt.show()