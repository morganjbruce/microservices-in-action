from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from FEES SERVICE ..."


@app.route("/health")
def health():
    return "ping"
