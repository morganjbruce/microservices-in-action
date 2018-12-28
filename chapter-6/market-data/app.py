import socket

from flask import Flask, jsonify

app = Flask(__name__)

PRICES = {
    'BHP': {'Code': 'BHP', 'Price': 91.72},
    'GOOG': {'Code': 'GOOG', 'Price': 34.21},
    'ABC': {'Code': 'ABC', 'Price': 1.17}
}


@app.route('/ping', methods=["GET"])
def ping():
    return socket.gethostname()


@app.route('/prices/<code>', methods=["GET"])
def price(code):
    exists = code in PRICES
    if exists:
        return jsonify(PRICES.get(code))
    else:
        return ('Not found', 404)


@app.route('/prices', methods=["GET"])
def all_prices():
    #raise Exception
    return jsonify(list(PRICES.values()))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
