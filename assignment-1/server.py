from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import time
import json
from datetime import datetime
import os
import requests



    # Set up the directory for assignment-1
assignment_dir = os.path.join(os.path.dirname(__file__), 'assignment-1')
os.makedirs(assignment_dir, exist_ok=True)  # Create directory if it doesn't exist


class UnreliableHandler(BaseHTTPRequestHandler):
    # Handling to GET requests
    def do_GET(self):
        if self.path == '/getbalance':
            self.handle_getbalance()
        elif self.path == '/getlogs':
            self.handle_getlogs()

    #handling /getbalanceroute 
    def handle_getbalance(self):
        #defining event outcome with the help of probabilities
        event_outcome = random.choices([200, 403, 500, 'timeout'], [0.5, 0.2, 0.1, 0.2])[0]
        if event_outcome == 'timeout':
            time.sleep(10) #simulating server timeout
            #adding a response indicating that the server timed out, so the client doesn't hang indefinitely
            self.send_error(504, "Gateway Timeout") #send 504 status
            self.log_event(504)  # Log timeout as 504 event
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
        self.log_event(event_outcome)

    #Handling the /getlogs route:
    def handle_getlogs(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        #reading the log file
        try:
            with open('log_file_path', 'r') as logfile:
                logs = json.load(logfile)  # Load the entire log file as JSON
                logs_json = json.dumps(logs)  # Convert logs to JSON string

                try:
                     self.wfile.write(logs_json.encode())  # Write the logs as a JSON response
                     self.wfile.flush()  # Ensure the data is sent to the client
                except ConnectionAbortedError:
                    print("Client disconnected while sending logs")

        except FileNotFoundError:
            self.wfile.write(json.dumps([]).encode())  # Return an empty list if no logs
            self.wfile.flush()  # Ensure data is sent
        
    # Log IP, timestamp, event outcome
    def log_event(self, outcome):
        assignment_dir = os.path.join(os.path.dirname(__file__), 'assignment-1')
        os.makedirs(assignment_dir, exist_ok=True)  # Create directory if it doesn't exist
   
    # Ensure the log file is created in the correct directory
        log_file_path = os.path.join(assignment_dir, 'log_file.json')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = self.client_address[0]
        log_entry = {'timestamp': timestamp, 'ip': ip, 'outcome': outcome}

    # Ensure the log file is a JSON array
        try:
            with open(log_file_path, 'r') as logfile:
                logs = json.load(logfile)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []  # Start with an empty list if the file does not exist or is empty
        logs.append(log_entry)  # Append the new log entry
        with open(log_file_path, 'w') as logfile:
            json.dump(logs, logfile, indent=4)  # Write logs back to the file

    
# Set up and start the server
def run(server_class=HTTPServer, handler_class=UnreliableHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__=="__main__":
    run()

    # Request balance
    response_balance = requests.get('http://localhost:8080/getbalance')
    print("Get Balance Response:")
    print(response_balance.text)

   # Request logs
    response_logs = requests.get('http://localhost:8080/getlogs')
    print("\nGet Logs Response:")
    print(response_logs.json())  # Assuming your logs are returned in JSON format