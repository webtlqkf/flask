from flask import Flask

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def hello_word():
        return '웹플시작!'
    return app