from flask import Flask

app = Flask(__name__)

PRICES = {
    'BHP': {'Code': 'BHP', 'Price': 91.72},
    'GOOG': {'Code': 'GOOG', 'Price': 34.21},
    'ABC': {'Code': 'ABC', 'Price': 1.17}
}


@app.route("/")
def hello():
    return "Hello from MARKET SERVICE ..."


@app.route("/health")
def health():
    return "ping"
