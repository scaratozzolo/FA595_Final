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

 The string in quotes can be used when defining a subset of services while performing a POST request on /nlp/services

### POST /api/services 

This endpoint allows a user to send a string of text to the server and receive a response containing the result of calling the services specified in the payload.

The payload must contain a text string, the subset of services as a list, as well as all of the other parameters that should be passed to each endpoint.
For example:

{"ticker": "your ticker", "tickers": ["list", "of", "tickers"], "services":["lstm_model", "allocation"]}

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

