import numpy as np

def mc_option_price(S, K, T, r, sigma, n_sims, option_type="call", seed=42):
    """Price a European option by simulating stock prices at expiry."""
    # same seed = same random numbers every run, so results are repeatable
    np.random.seed(seed)

    # one standard normal draw per simulation
    Z = np.random.standard_normal(n_sims)

    # simulated stock price at expiry for every path at once
    S_T = S * np.exp((r - 0.5 * sigma **2) * T + sigma * np.sqrt(T) * Z)

    # what the option pays in each simulation
    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    else:
        payoffs = np.maximum(K - S_T, 0)

    # discount factor applied to each payoff
    discounted = np.exp(-r * T) * payoffs

    price = discounted.mean()
    # standard error: how much the estimate could vary from run to run
    std_error = discounted.std() / np.sqrt(n_sims)

    return price, std_error

if __name__ == "__main__":
    bs_price = 10.4506
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        price, se = mc_option_price(100, 100, 1, 0.05, 0.2, n)
        low, high = price - 1.96 * se, price + 1.96 * se
        inside = low <= bs_price <= high
        print(f"{n:>9,} sims: {price:.4f}  95% CI [{low:.4f}, {high:.4f}]  contains BS: {inside}")