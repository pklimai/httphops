#!/usr/bin/python3

import os
import socket
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from requests.exceptions import ConnectionError, ConnectTimeout


DEFAULT_ADDR_LISTEN = "0.0.0.0"
DEFAULT_PORT_LISTEN = 8000
DEFAULT_ADDR_REQUEST = None
DEFAULT_PORT_REQUEST = 80


class HTTPHopsRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        body_text = "HTTPHops server: Hostname={}, Server IP={}, Client IP={} <br>\n"\
            .format(socket.gethostname(), socket.gethostbyname(socket.gethostname()), self.address_string())

        request_addr = os.environ.get("ADDR_REQUEST") or DEFAULT_ADDR_REQUEST
        request_port = int(os.environ.get("PORT_REQUEST") or DEFAULT_PORT_REQUEST)

        if request_addr is not None:
            try:
                body_text += "Response from the next tier: <br>\n"
                resp = requests.get("http://{}:{}".format(request_addr, str(request_port))).text
                body_text += resp + "<br>\n"
            except (ConnectionError, ConnectTimeout):
                body_text += "Error connecting." + "<br>\n"

        self.wfile.write(body_text.encode("utf8"))


if __name__ == "__main__":
    listen_addr = os.environ.get("ADDR_LISTEN") or DEFAULT_ADDR_LISTEN
    listen_port = int(os.environ.get("PORT_LISTEN") or DEFAULT_PORT_LISTEN)

    httpd = HTTPServer((listen_addr, listen_port), HTTPHopsRequestHandler)

    print("Starting httpd server on {}:{}".format(listen_addr, listen_port))
    httpd.serve_forever()
