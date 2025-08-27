"""A simple python application to get node information"""

import time
import os

from http import HTTPStatus
from functools import cache
from flask import Flask, Request, request, render_template
app = Flask(__name__)

@app.route("/")
def index() -> str:
    """index route"""
    (is_allowed, status_code, reason) = get_request_allowed(request)
    if not is_allowed:
        return (reason, status_code)

    return (
        render_template("index.html.j2", server=get_server(), client=get_client(request)),
        status_code
    )

def get_server() -> dict:
    """returns server information"""
    return {
        "hostname": get_hostname(),
        "datetime": time.asctime(),
    }


def get_client(r: Request) -> dict:
    """returns client information"""
    return {
        "address": r.remote_addr,
        "real_address": get_ip(r),
        "method": r.method,
        "uri": r.url,
        "headers": r.headers,
    }

def get_ip(r: Request, resolve_headers: bool = True) -> str:
    """returns the IP from the request"""
    real_ip = r.remote_addr

    if resolve_headers:
        for header_name in ["X-Forwarded-For", "X-Real-IP"]:
            value = r.headers.get(header_name)
            if value is not None:
                real_ip = value

    # Check for an ipv6 mapped ipv4 address
    if real_ip.startswith('::ffff:'):
        real_ip = real_ip.removeprefix('::ffff:')

    return real_ip


def get_request_allowed(r: Request) -> (bool, HTTPStatus, str):
    """Check if a request is allowed to succeed"""
    denylist = get_denylist()
    iplist = [request.remote_addr, get_ip(r, True), get_ip(r, False)]
    
    for ip in iplist:
        if ip in denylist:
            reason = f"{ip} is not allowed"
            return False, HTTPStatus.FORBIDDEN, reason

    return True, HTTPStatus.OK, ""


@cache
def get_hostname() -> str:
    """return the hostname"""
    hostname = ""
    if os.environ.get("HOSTNAME", None):
        return os.environ.get("HOSTNAME")
    
    with open("/etc/hostname", encoding="utf-8") as f:
        hostname = f.read().strip(" \t\n\r")

    return hostname

@cache
def get_denylist() -> list[str]:
    """Returns the denylist"""
    denylist = []
    if os.environ.get("DENYLIST"):
        for ip in os.environ.get("DENYLIST", "").split(','):
            denylist.append(ip)

    return denylist

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_RUN_HOST", "0.0.0.0"),
        port=os.environ.get("FLASK_RUN_PORT", "8080"),
        debug=os.environ.get("FLASK_DEBUG"),
    )
