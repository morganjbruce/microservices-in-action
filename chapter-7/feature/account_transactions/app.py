from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from ACCOUNT TRANSACTIONS SERVICE ..."


@app.route("/health")
def health():
    return "ping"
