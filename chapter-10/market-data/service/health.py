import socket
from service import app


@app.route('/ping', methods=["GET"])
def ping():
    return socket.gethostname()
