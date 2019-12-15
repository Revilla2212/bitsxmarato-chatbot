from flask import Flask
import chatbot
app = Flask(__name__)
@app.route("/hi")
def hi():
   return chatbot.init()
@app.route("/lang")
def info_lang():
   return chatbot.change_lang_init()
@app.route("/changelang/<name>")
def change_lang(name):
   return chatbot.change_lang(name)
