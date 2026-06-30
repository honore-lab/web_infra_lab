from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        try:
            a = int(params.get("a")[0])
            b = int(params.get("b")[0])
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing or invalid parameters")
            return

        if parsed.path == "/add":
            result = a + b
            operation = "addition"

        elif parsed.path == "/subtract":
            result = a - b
            operation = "subtraction"

        elif parsed.path == "/multiply":
            result = a * b
            operation = "multiplication"

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")
            return

        response = {
            "a": a,
            "b": b,
            "operation": operation,
            "result": result
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("localhost", 5000), MyServer)

print("Server running on http://localhost:5000")

server.serve_forever()