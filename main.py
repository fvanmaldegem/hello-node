"""A simple python application to get node information"""

import time
import os
from flask import Flask, Request, request, render_template

HOSTNAME = None
BLACKLISTED_IPS = []

with open("/etc/hostname", encoding="utf-8") as f:
    HOSTNAME = f.read().strip(" \t\n\r")

if os.environ.get("BLACKLISTED_IPS"):
    for ip in os.environ.get("BLACKLISTED_IPS", "").split(','):
        BLACKLISTED_IPS.append(ip)

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """index route"""
    real_ip = get_real_ip(request)
    if is_blacklisted(request):
        return f"Internal server error: {real_ip} is blacklisted", 500

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
    return {
        "address": r.remote_addr,
        "real_address": get_real_ip(r),
        "method": r.method,
        "uri": r.url,
        "headers": r.headers,
    }

def get_real_ip(r: Request) -> str:
    """returns the real IP from the request"""
    real_ip = r.remote_addr
    for header_name in ["X-Forwarded-For", "X-Real-IP"]:
        value = r.headers.get(header_name)
        if value is not None:
            real_ip = value

    # Check for an ipv6 mapped ipv4 address
    if real_ip.startswith('::ffff:'):
        real_ip = real_ip.removeprefix('::ffff:')

    return real_ip

def is_blacklisted(r: Request) -> bool:
    """checks if the request is blacklisted or not"""
    return get_real_ip(r) in BLACKLISTED_IPS

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_RUN_HOST", "0.0.0.0"),
        port=os.environ.get("FLASK_RUN_PORT", "8080"),
        debug=os.environ.get("FLASK_DEBUG"),
    )
