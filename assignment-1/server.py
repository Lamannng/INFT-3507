from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time
import json
from datetime import datetime
import os

# Define the assignment directory path
assignment_dir = os.path.join(os.getcwd(), 'assignment-1')  # Get the current working directory
os.makedirs(assignment_dir, exist_ok=True)  # Create directory if it doesn't exist

# Define the log file path within the assignment directory
log_file_path = os.path.join(assignment_dir, 'logfile.json')

class UnreliableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getbalance':
            self.handle_getbalance()
        elif self.path == '/getlogs':
            self.handle_getlogs()

    def handle_getbalance(self):
        event_outcome = random.choices([200, 403, 500, 'timeout'], [0.5, 0.2, 0.1, 0.2])[0]
        if event_outcome == 'timeout':
            time.sleep(10)  # Simulate timeout
            self.send_error(504, "Gateway Timeout")
            self.end_headers()
            self.log_event("timeout")
            return
        elif event_outcome == 403:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 Forbidden")
        elif event_outcome == 500:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Fake Balance Data</h1></body></html>")
        self.log_event(event_outcome)

    def handle_getlogs(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        try:
            with open(log_file_path, 'r') as logfile:
                logs = json.load(logfile)
                self.wfile.write(json.dumps(logs).encode())
        except FileNotFoundError:
            self.wfile.write(json.dumps([]).encode())  # Return empty list if no logs

    def log_event(self, outcome):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]
        log_entry = {'timestamp': timestamp, 'ip': ip, 'outcome': outcome}
        
        try:
            with open(log_file_path, 'r') as logfile:
                logs = json.load(logfile)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        logs.append(log_entry)
        with open(log_file_path, 'w') as logfile:
            json.dump(logs, logfile, indent=4)

# Set up and start the server
def run(server_class=HTTPServer, handler_class=UnreliableHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
