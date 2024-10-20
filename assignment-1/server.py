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
