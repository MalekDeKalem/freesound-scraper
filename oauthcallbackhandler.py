import urllib.parse
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    auth_code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/callback":
            query = urllib.parse.parse_qs(parsed.query)
            OAuthCallbackHandler.auth_code = query.get("code", [None])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>You may now return to the CLI application.</h1>")
        else:
            self.send_response(404)
            self.end_headers()


class OAuthServer:
    def __init__(self, port=5000):
        self.port = port

    def start_server(self):
        server = HTTPServer(("localhost", self.port), OAuthCallbackHandler)
        server.handle_request()

    def get_oauth_code(self, client_id):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        auth_url = (
            f"https://freesound.org/apiv2/oauth2/authorize/?"
            f"client_id={client_id}&response_type=code&redirect_uri=http://localhost:{self.port}/callback"
        )
        webbrowser.open(auth_url)

        server_thread.join()

        return OAuthCallbackHandler.auth_code
