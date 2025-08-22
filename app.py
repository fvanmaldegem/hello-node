import time
import socket
from flask import Flask, Request, request, render_template
from werkzeug.datastructures import EnvironHeaders

hostname = None
with open("/etc/hostname") as f:
    hostname = f.read().strip(' \t\n\r')

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return render_template('index.html.j2', server=get_server(), client=get_client(request))

def get_server() -> dict:
    return {
        'hostname': hostname,
        'datetime': time.asctime(),
    }

def get_client(request: Request) -> dict:
    real_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if real_ip is None: real_ip = request.environ.get('HTTP_X_REAL_IP')
    if real_ip is None: real_ip = request.remote_addr

    return {
        'address': request.remote_addr,
        'real_address': real_ip,
        'method': request.method,
        'uri': request.url,
        'headers': request.headers
    }

        