import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from cvxopt import matrix, solvers

def compute_VaR(tickers):
    n = len(tickers)   #count number of assets in the portfolio
    N = 10             #default time horizon to 10 days
    conf_level = 0.99  #default confident level to 99%
    z = norm.ppf(conf_level)
# 1. compute daily returns of the stocks in the portfolio:
    prices = yf.download(tickers, start=pd.Timestamp.today() - pd.DateOffset(years=1), progress=False)['Close']
    daily_ret = prices.pct_change().dropna()
# 2. compute average return of each asset:
    avg_ret = daily_ret.mean()
# check if portfolio has more than 1 asset...
    if n > 1:
    # 3. compute covariance matrix based on the returns:
        cov_matrix = daily_ret.cov()
        cov_matrix_annual = cov_matrix * 252
    # 4. compute initial portfolio mean:
        w_0 = [1 / n] * n  # initialize weights (set to equal weight)
        port_mean = avg_ret.dot(w_0)  # expected return of portfolio based on initial weights
    # 5. compute weights using Markowitz Portfolio Optimization (solve a quadratic program):
        Q = cov_matrix.to_numpy()
        P = matrix(Q)
        q = matrix(np.zeros(n))
        b = matrix(np.array([1., port_mean]))
        A = np.ones((2, n))
        A[1, :] = avg_ret
        A = matrix(A)
        optsol = solvers.qp(P, q, A=A, b=b)
        w = np.array(optsol['x']).flatten()
    # 6. re-compute portfolio mean with optimal weights:
        port_mean_opt = avg_ret.dot(w)
    # 7. compute portfolio volatility with optimal weights (sd of portfolio):
        port_sd_opt = np.sqrt(w.T.dot(cov_matrix_annual).dot(w))
    # 8. compute VaR:
        # Formula:
        # N-day VaR = 1-day VaR * sqrt(N)
        # 1-day VaR = investment_value * sd * z-value
        VaR_1 = port_mean_opt * port_sd_opt * z
        VaR_N = round(VaR_1 * np.sqrt(N), 4)
        w = np.round(np.array(w * 100), decimals=2)
        w = list(map("{}%".format, w))
    else:
        port_mean_opt = avg_ret
        port_sd_opt = np.sqrt(daily_ret.var())
        VaR_1 = port_mean_opt * port_sd_opt * z
        VaR_N = round(VaR_1 * np.sqrt(N), 4)
        w = ["{:.0%}".format(1)]
    df = pd.DataFrame(data={"Col1": tickers, "Col2": w})
    df.loc[len(df)] = ["portfolio mean", "{}%".format(np.round(port_mean_opt*100, decimals=2))]
    df.loc[len(df)] = ["portfolio volatility", "{}%".format(np.round(port_sd_opt*100, decimals=2))]
    out_string = ("10-day VaR at 99% confidence level is " + str(VaR_N) + ", given the weight of each asset, portfolio mean, and portfolio volatility above.")
    return [df.to_json(orient = 'split'), out_string]


#if __name__ == '__main__':
#    print(compute_VaR(['AAPL', 'FB', 'AMZN', 'MRNA','SBUX', 'NKE']))