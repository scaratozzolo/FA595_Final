from flask import jsonify, request, url_for
from app import app
# This line import your functions from the services folder
from app.services import *


@app.route("/")
def index():

    resp = """FA595 Final Fall 2021
    <br /><br />
    Natalia Azarian<br />
    Scott Caratozzolo<br />
    Audrey Nguyen<br />
    Agathe Sadeghi
    <br /><br />
    More information and documentation: <a href='https://github.com/scaratozzolo/FA595_Final'>https://github.com/scaratozzolo/FA595_Final</a>"""

    return resp


@app.route("/api", methods=["POST"])
def nlp():
    # Whatever you send to the server will then print in the console
    print(request.json)

    # Whatever you send to the server will be returned back from the api
    return jsonify(request.json)

@app.route("/api/services", methods=["GET", "POST"])
def services():

    __services = {
                "all": all_service,
                "lstm_model": lstm_service,
                "beta": beta_service,
                "sharpe": sharpe_service
                "beta_allocation": beta_allocation_service,
                "compute_VaR": compute_VaR_service
        }

    if request.method == "GET":
        return jsonify({"services": {k:url_for(v.__name__) for k,v in __services.items()}})

    elif request.method == "POST":

        data = request.json

        if "services" not in data:
            return jsonify({"error": "no services defined in request"})

        response = {}

        for service in data['services']:

            if service in __services:

                response[service] = __services[service](data).get_json()

        return jsonify(response)

@app.route("/api/services/all", methods=["POST"])
def all_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    services = {}
    services["lstm_model"] = lstm_service(data).get_json()
    services["beta"] = beta_service(data).get_json()
    services["sharpe"] = sharpe_service(data).get_json()
    services["beta_allocation"] = beta_allocation_service(data).get_json()
    services["compute_VaR"] = compute_VaR_service(data).get_json()

    return jsonify(services)

@app.route("/api/services/lstm_model", methods=["POST"])
def lstm_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "ticker" not in data:
        return jsonify({"error":"'ticker' missing from payload"})

    return jsonify(lstm_model(ticker=data['ticker']))


@app.route("/api/services/beta_allocation", methods=["POST"])
def beta_allocation_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "tickers" not in data:
        return jsonify({"error":"'tickers' missing from payload"})
    elif type(data["tickers"]) is not list:
        return jsonify({"error":"'tickers' is not a list"})
    elif "beta" not in data:
        return jsonify({"error":"'beta' missing from payload"})

    return jsonify(PortOpt(tickers=data['tickers'], beta=data['beta']).allocate())

@app.route("/api/services/beta", methods=["POST"])
def beta_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "tickers" not in data:
        return jsonify({"error":"'tickers' missing from payload"})
    elif "start_dt" not in data:
        return jsonify({"error":"'start date' missing from payload"})
    elif "end_dt" not in data:
        return jsonify({"error":"'end date' missing from payload"})
    elif "inter" not in data:
        return jsonify({"error":"'interval' missing from payload"})
    # Check that two tickers are inputted
    elif len(data["tickers"]) != 2:
        return jsonify({"error":"input two tickers"})

    return jsonify(beta(tickers=data['tickers'], start_dt=data['start_dt'], end_dt=data['end_dt'], inter=data['inter']))

@app.route("/api/services/sharpe", methods=["POST"])
def sharpe_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "tickers" not in data:
        return jsonify({"error":"'tickers' missing from payload"})
    elif "start_dt" not in data:
        return jsonify({"error":"'start date' missing from payload"})
    elif "end_dt" not in data:
        return jsonify({"error":"'end date' missing from payload"})
    elif "inter" not in data:
        return jsonify({"error":"'interval' missing from payload"})
    elif "weights" not in data:
        return jsonify({"error":"'weights' missing from payload"})
    elif type(data["tickers"]) is not list:
        return jsonify({"error":"'tickers' is not a list"})
    # Check that weight inputted for each symbol
    elif len(data["weights"]) != len(data["tickers"]):
        return jsonify({"error":"enter a weight for each ticker"})
    # Check that weights = 1
    if sum(data["weights"]) != 1:
        return jsonify({"error":"check that weights total 100%"})

    return jsonify(sharpe(tickers=data['tickers'], start_dt=data['start_dt'], end_dt=data['end_dt'], inter=data['inter'], weights=data['weights']))

  @app.route("/api/services/compute_VaR", methods=["POST"])
def compute_VaR_service(data=None):
    if not data:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"})

    if "tickers" not in data:
        return jsonify({"error": "'tickers' missing from payload"})
    elif type(data["tickers"]) is not list:
        return jsonify({"error":"'tickers' is not a list"})

    return jsonify(compute_VaR(tickers=data['tickers']))
