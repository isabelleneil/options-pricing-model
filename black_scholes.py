
import numpy as np
import scipy.stats as si

class BlackScholesModel:
    def __init__(self, S, K, T, r, sigma):
     self.S = S            # underlying price
     self.K = K            # option strike
     self.T = T            # time to expiration
     self.r = r            # risk free interest rate
     self.sigma = sigma    # volatility of underlying

    def d1(self):
       return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
       return self.d1() - self.sigma * np.sqrt(self.T)

    def call_option_price(self):
       return (self.S * si.norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * si.norm.cdf(self.d2()))

    def put_option_price(self):
       return (self.K * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2()) - self.S * si.norm.cdf(-self.d1()))

    def put_call_parity_check(self):
          lhs = self.call_option_price() - self.put_option_price()
          rhs = self.S - self.K * np.exp(-self.r * self.T)
          diff = abs(lhs-rhs)
          return lhs, rhs, diff

if __name__ == "__main__":
   bsm = BlackScholesModel (S=100, K=100, T=1, r=0.05, sigma=0.2)
   print("Call:", bsm.call_option_price())
   print("Put:", bsm.put_option_price())
   print("Parity check:", bsm.put_call_parity_check())