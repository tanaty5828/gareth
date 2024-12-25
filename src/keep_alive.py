from flask import Flask, request
from threading import Thread

app = Flask("")


@app.route("/", methods=["GET", "HEAD"])
def home():
    if request.method == "HEAD":
        app.logger.info("HEAD request received")
    return "I'm alive"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
