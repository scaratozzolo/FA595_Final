import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


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

    train_score = mean_squared_error(y, train_predict)

    prediction = model.predict(dataset[-1].reshape(-1,1))
    prediction = scaler.inverse_transform(prediction)

    return {"prediction": float(prediction[0][0]), "mse": float(train_score)}


if __name__ == '__main__':
    import json
    t = lstm_model("AAPL")
    print(json.dumps(t))