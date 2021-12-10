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
                "allocation": allocation_service,
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
    services["allocation"] = allocation_service(data).get_json()

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


@app.route("/api/services/allocation", methods=["POST"])
def allocation_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "tickers" not in data:
        return jsonify({"error":"'tickers' missing from payload"})
    elif type(data["tickers"]) is not list:
        return jsonify({"error":"'tickers' is not a list"})

    return jsonify(PortOpt(tickers=data['tickers']).allocate())

@app.route("/api/services/beta", methods=["POST"])
def beta_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "ticker" not in data:
        return jsonify({"error":"'ticker' missing from payload"})

    return jsonify(Beta(ticker=data['ticker']))

@app.route("/api/services/sharpe", methods=["POST"])
def sharpe_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "ticker" not in data:
        return jsonify({"error":"'ticker' missing from payload"})

    return jsonify(Sharpe(ticker=data['ticker']))