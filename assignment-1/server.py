import http.server
import socketserver
import random
import json
import time
from datetime import datetime

# Set the port for the server
PORT = 8080

# Log file to store request data
log_file = 'logfile.json'

# Handler for HTTP requests
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_event(self, ip_address, status_code):
        """Logs the event to a JSON file with timestamp, IP address, and status code."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'status_code': status_code
        }
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def do_GET(self):
        ip_address = self.client_address[0]

        if self.path == '/getbalance':
            outcome = random.choices(
                population=[200, 403, 500, 'timeout'],
                weights=[50, 20, 10, 20],
                k=1
            )[0]

            if outcome == 'timeout':
                # Simulate a timeout by not responding
                self.log_event(ip_address, 'timeout')
                time.sleep(5)
                return

            if outcome == 200:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Your Balance: $1000</h1></body></html>")
                self.log_event(ip_address, 200)
            elif outcome == 403:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                self.log_event(ip_address, 403)
            elif outcome == 500:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")
                self.log_event(ip_address, 500)

        elif self.path == '/getlogs':
            try:
                with open(log_file, 'r') as f:
                    logs = [json.loads(log) for log in f.readlines()]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(logs).encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")

# Start the server
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
