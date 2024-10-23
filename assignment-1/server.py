import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import random

class RequestHandler(BaseHTTPRequestHandler):
    log_file_path = os.path.join(os.path.dirname(__file__), 'logfile.json')

    def do_GET(self):
        if self.path == '/getbalance':
            self.handle_getbalance()
        elif self.path == '/getlogs':
            self.handle_getlogs()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_getbalance(self):
        event_outcome = random.choice(['success', 'failure'])
        
        if event_outcome == 'failure':
            self.send_response(403)
            self.end_headers()
            self.log_event('403 Forbidden')
            return
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Fake Balance Data</h1></body></html>')
        self.log_event('success')

    def handle_getlogs(self):
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'r') as logfile:
                logs = json.load(logfile)
        else:
            logs = []

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(logs).encode('utf-8'))

    def log_event(self, event_outcome):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as logfile:
                json.dump([], logfile)  # Initialize with an empty list

        with open(self.log_file_path, 'r+') as logfile:
            logs = json.load(logfile)
            logs.append({'event': event_outcome})
            logfile.seek(0)
            json.dump(logs, logfile)

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port 8080...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
