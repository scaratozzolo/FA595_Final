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
                # "chat_bot": chat_bot_service,
                # "next_word": next_word_service,
                # "word_freq": word_frequency_service,
                # "word_lem": word_lemmatization_service,
                # "entity_ext": entity_ext_service,
                # "text_sentiment": text_sentiment_service,
                # "spellcheck": spellcheck_service,
                # "translate": translate_service
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
    # services["chat_bot"] = chat_bot_service(data).get_json()
    # services["next_word"] = next_word_service(data).get_json()
    # services["word_freq"] = word_frequency_service(data).get_json()
    # services["word_lem"] = word_lemmatization_service(data).get_json()
    # services["entity_ext"] = entity_ext_service(data).get_json()
    # services["text_sentiment"] = text_sentiment_service(data).get_json()
    # services["spellcheck"] = spellcheck_service(data).get_json()
    # services["translate"] = translate_service(data).get_json()

    return jsonify(services)

@app.route("/api/services/template", methods=["POST"])
def template_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "text" not in data:
        return jsonify({"error":"'text' missing from payload"})

    return jsonify(template(text=data['text']))


