from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time
import json
from datetime import datetime

class UnreliableHandler(BaseHTTPRequestHandler):
    # Handling to GET requests
    def do_GET(self):
        if self.path == '/getbalance':
            self.handle_getbalance()
        elif self.path == '/getlogs':
            self.handle_getlogs()

    #handling /getbalanceroute 
    def handlegetbalance(self):
        #defining event outcome with the help of probabilities
        event_outcome = random.choices([200, 403, 500, 'timeout'], [0.5, 0.2, 0.1, 0.2])[0]
        if event_outcome == 'timeout':
            time.sleep(10) #simulating server timeout
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
        #logging the outcome
        self.log_event(outcome)


    #Handling the /getlogs route:
    def handle_getlogs(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        #reading the log file
        try:
            with open('logfile.json', 'r') as logfile:
                logs = logfile.readlines()
                #conerting logs to json list
                logs_json = [json.loads(log.strip()) for log in logs]
                self.wfile.write(json.dumps(logs_json).encode())
        except FileNotFoundError:
            self.wfile.write(json.dumps([]).encode()) # Returning an empty list if no logs



        