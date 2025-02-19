import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

def beta(tickers, start_dt, end_dt, inter):

    # Import daily adjusted close (stock price) data for specific tickers and date range / interval
    data = yf.download(tickers, start=start_dt, end=end_dt, interval=inter)['Adj Close']
    
    # Convert historical stock prices to daily percent change
    price_change = data.pct_change()
    
    # Drop NaN
    df = price_change.dropna()
    
    # Create arrays for x and y variables in the regression model
    # Linear regression will only apply to first two tickers inputted
    x = np.array(df.iloc[:, 0]).reshape((-1,1))
    y = np.array(df.iloc[:, 1])
    
    # Define the model and type of regression
    model = LinearRegression().fit(x, y)

    return {"Beta": float(model.coef_)}

def sharpe(tickers, start_dt, end_dt, inter, weights):

    # Import daily adjusted close (stock price) data for specific tickers and date range / interval
    data = yf.download(tickers, start=start_dt, end=end_dt, interval=inter)['Adj Close']

    # Calculate log return of the portfolio
    log_return = np.sum(np.log(data/data.shift())*weights, axis=1)
    
    # Calculate the Sharpe Ratio
    sharpe_ratio = log_return.mean()/log_return.std()

    return {"Sharpe Ratio": sharpe_ratio}
 

# tickers = ['SPY', 'AXS'] # input x-variable first
# start_dt = '2020-02-22' # input as YYYY-MM-DD
# end_dt = '2020-03-22' # input as YYYY-MM-DD
# inter = '1d' # specify the interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo

# weights = [0.5, 0.5] # assign weights in order of tickers specified

# if __name__ == '__main__':
#     print(Beta(ticker, start_dt, end_dt, inter))
#     print(Sharpe(ticker, start_dt, end_dt, inter, weights))
