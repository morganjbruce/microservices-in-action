import os
import socket
import time
from flask import Flask
from flask import jsonify
from holdings import queries_cached

app = Flask(__name__)

@app.route('/ping', methods=["GET"])
def ping():
    return socket.gethostname()

@app.route('/holdings', methods=["GET"])
def holdings():
    query = queries_cached.Holdings()

    return jsonify(query.all())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
