from flask import Flask, request


def run_func_local(func):
    app = Flask(__name__)

    @app.route('/')
    def invoke_func():
        return func(request)

    app.run('127.0.0.1', 8000, debug=True)
