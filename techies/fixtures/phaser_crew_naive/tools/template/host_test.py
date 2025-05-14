import http.server
import socketserver
import os

PORT = 8000
# get the directory of the current file
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on http://localhost:{PORT} from {DIRECTORY}")
    httpd.serve_forever()
