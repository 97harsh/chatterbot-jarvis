"""Main App used for chatbot."""

import spacy
try:
    nlp = spacy.load("en")
except OSError:
    from spacy.cli import download
    download("en")


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
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
# chatbot.set_trainer(ChatterBotCorpusTrainer)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')
# dir = os.path.join('/home/$USER/anaconda3/envs/chatbot/lib',
#    'python3.6/site-packages/chatterbot_corpus/data/english')
# assert os.path.exists(dir), f"path not found {dir}"
# trainer.train(dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    return str(chatbot.get_response(userText))


def main():
    print(chatbot.get_response(""))
    while True:
        question = input()
        response = chatbot.get_response(question)
        print(response)


if __name__ == '__main__':
    # main()
    app.run()
