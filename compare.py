from black_scholes import BlackScholesModel
from get_options import get_option_data
from market_inputs import get_risk_free_rate, get_time_to_expiry, get_historical_volatility

# 1. Pull the data and model inputs
calls, puts,  S, expiry = get_option_data("AAPL", 30)
T = get_time_to_expiry(expiry)
r = get_risk_free_rate()
sigma = get_historical_volatility("AAPL")

print(f"Expiry {expiry} | S={S:.2f} | T={T:.3f} | r={r:.4f} | sigma={sigma:.4f}")

# 2. Keep strikes within 15% of the stock price
# (far out strikes trade rarely, so their quotes are unreliable)
calls = calls[(calls["strike"] > 0.85 * S) & (calls["strike"] < 1.15 * S)].copy()

# 3. Market price = midpoint of bid and ask
calls["market_mid"] = (calls["bid"] + calls["ask"]) / 2

# 4. Model price for each strike
model_prices = []
for K in calls["strike"]:
    bsm = BlackScholesModel(S=S, K=K, T=T, r=r, sigma=sigma)
    model_prices.append(bsm.call_option_price())
calls["model_price"] = model_prices

# 5. How far off the model is
calls["difference"] = calls["model_price"] - calls["market_mid"]

print(calls[["strike", "market_mid", "model_price", "difference"]].round(2))