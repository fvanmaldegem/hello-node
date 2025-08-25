"""A simple python application to get node information"""

import time
import os
from flask import Flask, Request, request, render_template

HOSTNAME = None

with open("/etc/hostname", encoding="utf-8") as f:
    HOSTNAME = f.read().strip(" \t\n\r")

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """index route"""
    return render_template(
        "index.html.j2", server=get_server(), client=get_client(request)
    )


def get_server() -> dict:
    """returns server information"""
    return {
        "hostname": HOSTNAME,
        "datetime": time.asctime(),
    }


def get_client(r: Request) -> dict:
    """returns client information"""
    real_ip = r.remote_addr
    for header_name in ["X-Forwarded-For", "X-Real-IP"]:
        value = r.headers.get(header_name)
        if value is not None:
            real_ip = value

    return {
        "address": r.remote_addr,
        "real_address": real_ip,
        "method": r.method,
        "uri": r.url,
        "headers": r.headers,
    }

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_RUN_HOST", "0.0.0.0"),
        port=os.environ.get("FLASK_RUN_PORT", "8080"),
        debug=os.environ.get("FLASK_DEBUG"),
    )
