from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_word():
    return '웹플시작!'