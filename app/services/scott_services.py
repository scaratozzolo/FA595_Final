import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import scipy.optimize as opt


def lstm_model(ticker):

    data = yf.download(ticker, start=pd.Timestamp.today() - pd.DateOffset(years=1), progress=False)

    scaler = MinMaxScaler()
    dataset = scaler.fit_transform(data["Adj Close"].ravel().reshape(-1,1))
    x = dataset[:-1,0].reshape(-1,1)
    y = dataset[1:,0].reshape(-1,1)

    model = Sequential()
    model.add(LSTM(4, input_shape=x.shape))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x, y, epochs=20, batch_size=1, verbose=2)

    train_predict = model.predict(x)
    train_predict = scaler.inverse_transform(train_predict)
    y = scaler.inverse_transform(y)

    train_score = np.sqrt(mean_squared_error(y, train_predict))

    prediction = model.predict(dataset[-1].reshape(-1,1))
    prediction = scaler.inverse_transform(prediction)

    return {"prediction": float(prediction[0][0]), "rmse": float(train_score)}



class PortOpt:

    def __init__(self, tickers, beta):
        
        self.tickers = tickers
        self.beta_target = beta
        self.data = yf.download(self.tickers, start=pd.Timestamp.today() - pd.DateOffset(years=1), progress=False)["Adj Close"]

        self.rets = self.data.pct_change()


        self.bench_data = yf.download("SPY", start=pd.Timestamp.today() - pd.DateOffset(years=1), progress=False)["Adj Close"]
        self.bench_rets = self.bench_data.pct_change()

        t = pd.concat([self.bench_rets, self.rets], axis=1)

        # Betas vector
        hist_covs = np.array(t.cov().iloc[0])
        bench_var = hist_covs[0]
        self.beta_vec = hist_covs[1:]/bench_var
        

    def _get_ret_vol_sr(self, weights):
        """
        Calculates the returns, volatility, and sharpe of a portfolio with given weights
        """
        weights = np.array(weights)
        ret = np.sum(self.rets.mean() * weights) * 252
        vol = np.sqrt(np.dot(weights.T, np.dot(self.rets.cov()*252, weights)))
        sr = ret/vol
        return np.array([ret, vol, sr])

    def _neg_sharpe(self, weights):
        return self._get_ret_vol_sr(weights)[2] * -1

    def allocate(self):

        cons = ({'type':'eq', 'fun': lambda x: np.sum(x)-1},
                {'type':'eq', 'fun': lambda x: np.dot(self.beta_vec, x)-self.beta_target})

        bounds = tuple((0,1) for _ in range(len(self.tickers)))
        init_guess = [1/len(self.tickers) for _ in range(len(self.tickers))]

        opt_results = opt.minimize(self._neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
        
        return {"results": {k:v for k,v in zip(self.rets.columns.to_list(), opt_results.x.round(3).tolist())}, "sharpe": opt_results.fun.round(3)*-1, 
                "calculated_beta": np.dot(self.beta_vec, opt_results.x).round(3), "success": str(opt_results.success)}




if __name__ == '__main__':
    # import json
    # t = lstm_model("AAPL")
    # print(json.dumps(t))

    print(PortOpt(['AAPL', 'FB', 'AMZN', 'MRNA','SBUX', 'NKE'], 1).allocate())