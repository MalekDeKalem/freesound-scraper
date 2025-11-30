import urllib
import threading
import http.server
from http.server import BaseHTTPRequestHandler
import webbrowser


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/callback":
            query = urllib.parse.parse_qs(parsed.query)
            self.code = query.get("code", [None])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>You may now return to the CLI application.</h1>")

    def start_server(self):
        server = HTTPServer(("localhost", 5000), OAuthCallbackHandler)
        server.handle_request()

    def get_oauth_code(self, client_id):
        thread = threading.Thread(target=start_server)
        thread.start()

        auth_url = (
            f"https://freesound.org/apiv2/oauth2/authorize/"
            f"?client_id={client_id}"
            f"&response_type=code"
            f"&redirect_uri=http://localhost:5000/callback"
        )
        webbrowser.open(auth_url)

        thread.join()

        return self.code

