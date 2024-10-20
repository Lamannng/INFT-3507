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