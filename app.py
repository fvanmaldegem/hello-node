"""A simple python application to get node information"""

import time
from flask import Flask, Request, request, render_template

HOSTNAME = None

with open("/etc/hostname", encoding="utf-8") as f:
    HOSTNAME = f.read().strip(" \t\n\r")

app = Flask(__name__)

@app.route("/")
def index() -> str:
    """index route"""
    return render_template(
        "index.html.j2",
        server=get_server(),
        client=get_client(request)
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
    for header_name in ["HTTP_X_FORWARDED_FOR", "HTTP_X_REAL_IP"]:
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
