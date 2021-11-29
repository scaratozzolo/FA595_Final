from flask import jsonify, request, url_for
from app import app
import requests
# This line import your functions from the services folder
from app.services import *


@app.route("/")
def index():

    resp = """FA595 Midterm Fall 2021
    <br /><br />
    Natalia Azarian<br />
    Scott Caratozzolo<br />
    Audrey Nguyen<br />
    Agathe Sadeghi
    <br /><br />
    More information and documentation: <a href='https://github.com/scaratozzolo/FA595_Midterm'>https://github.com/scaratozzolo/FA595_Midterm</a>"""

    return resp


@app.route("/nlp", methods=["POST"])
def nlp():
    # Whatever you send to the server will then print in the console
    print(request.json)

    # Whatever you send to the server will be returned back from the api
    return jsonify(request.json)

@app.route("/nlp/services", methods=["GET", "POST"])
def services():

    __services = {
                "all": all_service,
                "chat_bot": chat_bot_service,
                "next_word": next_word_service,
                "word_freq": word_frequency_service,
                "word_lem": word_lemmatization_service,
                "entity_ext": entity_ext_service,
                "text_sentiment": text_sentiment_service,
                "spellcheck": spellcheck_service,
                "translate": translate_service
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

@app.route("/nlp/services/all", methods=["POST"])
def all_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    services = {}
    services["chat_bot"] = chat_bot_service(data).get_json()
    services["next_word"] = next_word_service(data).get_json()
    services["word_freq"] = word_frequency_service(data).get_json()
    services["word_lem"] = word_lemmatization_service(data).get_json()
    services["entity_ext"] = entity_ext_service(data).get_json()
    services["text_sentiment"] = text_sentiment_service(data).get_json()
    services["spellcheck"] = spellcheck_service(data).get_json()
    services["translate"] = translate_service(data).get_json()

    return jsonify(services)

@app.route("/nlp/services/chat_bot", methods=["POST"])
def chat_bot_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    chat_id = None

    if "text" not in data:
        return jsonify({"error":"'text' missing from payload"})
    elif "chat_id" in data:
        try:
            chat_id = int(data['chat_id'])
        except:
            return jsonify({"error":f"invalid 'chat_id' in payload. given: {data['chat_id']}, type: {type(data['chat_id'])}"})

    return jsonify(chat_bot(text=data['text'], chat_id=chat_id))


@app.route("/nlp/services/next_word", methods=["POST"])
def next_word_service(data=None):
    
    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    k = 5
    if "text" not in data:
        return jsonify({"error":"'text' missing from payload"})
    elif "num_words" in data:
        try:
            k = int(data['num_words'])
        except:
            return jsonify({"error":f"invalid 'num_words' in payload. given: {data['num_words']}, type: {type(data['num_words'])}"})

    return jsonify(next_word(text=data['text'], k=k))


@app.route("/nlp/services/word_freq", methods=["POST"])
def word_frequency_service(data=None):
    
    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})

    return jsonify(word_freq(text=data['text']))


@app.route("/nlp/services/word_lem", methods=["POST"])
def word_lemmatization_service(data=None):
    
    if not data:
        data = request.json
        if not data:
            return jsonify({"error":"no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})

    return jsonify(word_lem(text=data['text']))

@app.route("/nlp/services/entity_ext", methods=["POST"])
def entity_ext_service(data=None):

    if not data:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})

    return jsonify(entity_ext(text=data['text']))


@app.route("/nlp/services/text_sentiment", methods=["POST"])
def text_sentiment_service(data=None):
    if not data:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})

    return jsonify(text_sentiment(text=data['text']))

@app.route("/nlp/services/spellcheck", methods=["POST"])
def spellcheck_service(data=None):
    if not data:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})

    return jsonify(spellcheck(text=data['text']))

@app.route("/nlp/services/translate", methods=["POST"])
def translate_service(data=None):
    if not data:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"})

    if "text" not in data:
        return jsonify({"error": "'text' missing from payload"})
    elif "language_code" not in data:
        return jsonify({"error":"'language_code' missing from payload"})

    return jsonify(translate(text=data['text'], language=data['language_code']))
