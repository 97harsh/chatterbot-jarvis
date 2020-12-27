"""Main App used for chatbot."""

import spacy
try:
    nlp = spacy.load("en")
except Exception:
    from spacy.cli import download
    download("en")

import os
import logging

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
app = Flask(__name__, template_folder="templates")
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
chatbot = ChatBot('JARVIS',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=[
                                  'chatterbot.logic.MathematicalEvaluation',
                                  'chatterbot.logic.TimeLogicAdapter',
                                  'chatterbot.logic.BestMatch',
                                  {'import_path': 'chatterbot.logic.BestMatch',
                                   'default_response': 'I am sorry, but I do not understand.\
                                        I am still learning.',
                                   'maximum_similarity_threshold': 0.90
                                   }
                  ])  # create chatbot

# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.english')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}"


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    return str(chatbot.get_response(userText))
    # return f"Hi,  I am fine!!{UserText}"


# def main():
#     print(chatbot.get_response(""))
#     while True:
#         question = input()
#         response = chatbot.get_response(question)
#         print(response)


if __name__ == '__main__':
    # main()
    app.run()
