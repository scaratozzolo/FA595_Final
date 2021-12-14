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
 - "beta" : /api/services/beta
 - "sharpe" : /api/services/sharpe

 The string in quotes can be used when defining a subset of services while performing a POST request on /api/services

### POST /api/services 

This endpoint allows a user to send a string of text to the server and receive a response containing the result of calling the services specified in the payload.

The payload must contain a text string, the subset of services as a list, as well as all of the other parameters that should be passed to each endpoint.
For example:

{"ticker": "your ticker", "tickers": ["list", "of", "tickers"], "services":["lstm_model", "allocation", "beta", "sharpe"]}

### POST /api/services/all

The all endpoint allows a user to send a string of text to the server and receive back a response containing the result of calling all the other endpoints.

This endpoint can only be accessed through a POST request. The payload must contain a text string as well as all of the other parameters that should be passed to each endpoint. For example:

{"ticker": "your ticker", "tickers": ["list", "of", "tickers"]}

Response from the server will look like:

{
  "lstm_model": {
    ...
  }, 
  "allocation": {
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

{"prediction": float, "mse": float}


### POST /api/services/allocation

The allocation endpoint allows a user to send a list of tickers to the server and recieve the max Sharpe allocation percentages.

This endpoint can only be accessed through a POST request. The payload must be in the form of: 

{"tickers": ["list", "of", "tickers"]}

Response from the server will look like:

{'results': {"ticker": float}, 'sharpe': float}

The order of the ticker percentages is found in the tickers key. This is because during data collection the tickers are alphabetized.


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

{"Sharpe Ratio": float}
