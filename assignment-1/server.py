import http.server
import socketserver
import random
import json
import time
from datetime import datetime

# Port for server (adjustable)
PORT = 8080  # Use an available port

# File for storing log data
log_file = 'logfile.json'

class UnreliableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_event(self, ip_address, status_code):
        """
        Logs each event with timestamp, IP address, and status code.
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'status_code': status_code
        }
        
        # Read existing log entries
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        # Append new log entry
        logs.append(log_entry)

        # Write all log entries back to the log file as a JSON array
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)

    def do_GET(self):
        """
        Handles GET requests for both /getbalance and /getlogs routes.
        """
        ip_address = self.client_address[0]  # IP address of client
        
        # Handle /getbalance route with probability-based responses
        if self.path == '/getbalance':
            outcome = random.choices(
                population=['200', '403', '500', 'timeout'],
                weights=[50, 20, 10, 20],  # Probability distribution
                k=1
            )[0]
            
            if outcome == '200':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Your Balance: $1000</h1></body></html>")
                self.log_event(ip_address, 200)
            elif outcome == '403':
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                self.log_event(ip_address, 403)
            elif outcome == '500':
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")
                self.log_event(ip_address, 500)
            elif outcome == 'timeout':
                self.send_response(504)  # Gateway Timeout response
                self.end_headers()
                self.log_event(ip_address, 'timeout')
                time.sleep(5)  # Simulating delay

        # Handle /getlogs route to serve log file content in JSON format
        elif self.path == '/getlogs':
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)  # Read logs as JSON
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(logs, indent=4).encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Log file not found")
            except json.JSONDecodeError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Error reading log file")

# Start the server
with socketserver.TCPServer(("", PORT), UnreliableHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
