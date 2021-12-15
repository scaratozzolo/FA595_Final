# FA595_Final

## Deployment

Perform the following steps in a terminal or command prompt:

Clone this repo: ```git clone https://github.com/scaratozzolo/FA595_Final.git```

Then change directory into the repo: ```cd FA595_Final```

Install all the required packages: ```pip3 install -r requirements\requirements.txt```

Run the flask app: ```python3 run.py```

This will run the app on port 5000. This port must be open to incoming traffic. If the port is accepting requests, then you can use use go to http://your-public-ip:5000. If you're running the app locally, you just need to go to http://localhost:5000.

## Available Services

### GET /api/services

This endpoint will return a json object containing information regarding the available services.

The services available are as follows:

 - "all" : /api/services/all
 - "lstm_model" : /api/services/lstm_model
 - "max_ret" : /api/services/max_ret
 - "min_risk" : /api/services/min_risk
 - "beta" : /api/services/beta
 - "sharpe" : /api/services/sharpe
 - "beta_allocation" : /api/services/beta_allocation

 The string in quotes can be used when defining a subset of services while performing a POST request on /api/services

### POST /api/services 

This endpoint allows a user to send a string of text to the server and receive a response containing the result of calling the services specified in the payload.

The payload must contain a text string, the subset of services as a list, as well as all of the other parameters that should be passed to each endpoint.
For example:

{"ticker": "your ticker", "tickers": ["list", "of", "tickers"], "services":["lstm_model", "beta_allocation", "beta", "sharpe"]}


### POST /api/services/all

The all endpoint allows a user to send a string of text to the server and receive back a response containing the result of calling all the other endpoints.

This endpoint can only be accessed through a POST request. The payload must contain a text string as well as all of the other parameters that should be passed to each endpoint. For example:

{"ticker": "your ticker", "tickers": ["list", "of", "tickers"]}

Response from the server will look like:

{
  "lstm_model": {
    ...
  }, 
  "beta_allocation": {
    ...
  },
  "beta": {
    ...
  },
  "sharpe": {
    ...
  },
  ...
}

Each key in the response is equal to the values returned from /nlp/services.

### POST /api/services/lstm_model

The lstm_model endpoint allows a user to send a ticker to the server and have a long short term memory regression model be built using the previous one year of adjusted closes. The model will then predict the next day share price.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"ticker": "your ticker"}}

Response from the server will look like:

{"prediction": float, "rmse": float}


### POST /api/services/beta_allocation

The beta_allocation endpoint allows a user to send a list of tickers and a target beta to the server and recieve the max Sharpe allocation percentages while maintaining the target beta.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"tickers": ["list", "of", "tickers"], "beta": float}

Response from the server will look like:

{'results': {"ticker": float}, 'sharpe': float, 'calculated_beta': float, 'success': string_boolean}


### POST /api/services/compute_VaR

The compute_VaR endpoint allows a user to send a list of tickers to the server and receive the Value-at-Risk for every dollar invested, given a portfolio allocation, return, and volatility.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"tickers": ["list", "of", "tickers"]}

Response from the server will look like:

['{"columns":["Col1","Col2"],"index":[0,1,2,3],"data":[["ticker","%"],["ticker","%"],["portfolio mean","%"],["portfolio volatility","%"]]}', 
'10-day VaR at 99% confidence level is "VaR", given the weight of each asset, portfolio mean, and portfolio volatility above.']

### POST /api/services/beta

The beta endpoint allows a user to send a pair of tickers to the server to calculate the correlation between the stocks based on the adjusted close for a specific amount of time and interval. Note the interval codes are: 1d, 5d, 1wk, 1m, 2m, ...

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"ticker": ["x", "y"], "start date": 'YYYY-MM-DD', "end date": 'YYYY-MM-DD', "interval": 'see codes'}

Response from the server will look like:

{"Beta": float}


### POST /api/services/sharpe

The sharpe endpoint allows a user to send a list of tickers and associated weights to the server to calculate the sharpe ratio of the portfolio. Note each ticker requires a weight (entered in the order of the ticker list), and the sum of weights must equal 100%. Note the interval codes are: 1d, 5d, 1wk, 1m, 2m, ...

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"ticker": ["list", "of", "tickers"], "start date": 'YYYY-MM-DD', "end date": 'YYYY-MM-DD', "interval": 'see codes', "weights": [w1, w2, w3]}

Response from the server will look like:


### POST /api/services/max_ret

The max_return endpoint allows a user to send two tickers, their variance and the covariance between them to the server and have an output of efficient frontier based on maximizing the return of the two asset portfolio.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"tick1": "1st ticker", "tick2": "2nd ticker", "s1": "1st ticker's variance", "s2": "2nd ticker's variance", "cor":"covariance between the tickers"}

Response from the server will look like:

{"return": float, "risk": float}


### POST /api/services/min_risk

The max_return endpoint allows a user to send two tickers, their variance and the covariance between them to the server and have an output of efficient frontier based on minimizing the risk (variance) of the two asset portfolio.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"tick1": "1st ticker", "tick2": "2nd ticker", "s1": "1st ticker's variance", "s2": "2nd ticker's variance", "cor":"covariance between the tickers"}

Response from the server will look like:

{"return": float, "risk": float}

