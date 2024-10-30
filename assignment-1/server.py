import http.server
import socketserver
import random
import json
import time
from datetime import datetime
import requests
import sys

# Define server port
PORT = 8080  # Set this to the port number you wish to use

# Log file to store JSON logs for server events
log_file = 'logfile.json'

# Define the expected response code distribution
target_distribution = {'200': 50, '403': 20, '500': 10, 'timeout': 20}  # Target percentages for response codes
distribution_count = {'200': 0, '403': 0, '500': 0, 'timeout': 0}  # Track occurrences of each response type

class UnreliableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP request handler class to simulate an unreliable HTTP server
    with response codes (200, 403, 500) and timeouts.
    """

    def log_event(self, ip_address, status_code):
        """
        Logs each event with timestamp, IP address, and status code in JSON format.
        Writes each entry as a new line in the log file.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),  # Current time in ISO format
            "ip_address": ip_address,                 # IP address of the request origin
            "status_code": status_code                # Response status code for the event
        }

        # Append log entry as JSON on a new line in the log file
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def select_outcome(self):
        """
        Selects an outcome based on the target distribution.
        Controls response type frequencies over multiple requests to meet the target distribution.
        """
        # Generate a list of outcomes based on remaining quotas in target distribution
        remaining_choices = [
            outcome for outcome, target in target_distribution.items()
            for _ in range(target - distribution_count[outcome])
        ]

        # If all quotas are met, select randomly based on original probabilities
        if not remaining_choices:
            outcome = random.choices(
                ['200', '403', '500', 'timeout'],
                [0.5, 0.2, 0.1, 0.2]
            )[0]
        else:
            # Select outcome from remaining choices to meet exact target
            outcome = random.choice(remaining_choices)
        
        distribution_count[outcome] += 1  # Update count for selected outcome
        return outcome

    def do_GET(self):
        """
        Handles GET requests for both /getbalance and /getlogs routes.
        """
        ip_address = self.client_address[0]  # Retrieve client's IP address
        
        # Handle the /getbalance endpoint
        if self.path == '/getbalance':
            outcome = self.select_outcome()  # Select response outcome

            # Respond with 200 OK and a balance message
            if outcome == '200':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Your Balance: $1000</h1></body></html>")
                self.log_event(ip_address, 200)
            
            # Respond with 403 Forbidden
            elif outcome == '403':
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden")
                self.log_event(ip_address, 403)
            
            # Respond with 500 Internal Server Error
            elif outcome == '500':
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"500 Internal Server Error")
                self.log_event(ip_address, 500)
            
            # Simulate a timeout by not responding
            elif outcome == 'timeout':
                self.log_event(ip_address, 'timeout')
                time.sleep(5)  # Delay to simulate timeout
                return  # Exit without sending response
        
        # Handle the /getlogs endpoint
        elif self.path == '/getlogs':
            try:
                with open(log_file, 'r') as f:
                    logs = f.readlines()  # Read each log line
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write("".join(logs).encode())  # Send logs as text
            except FileNotFoundError:
                # Handle missing log file
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Log file not found")

# Initialize and start the server
with socketserver.TCPServer(("", PORT), UnreliableHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()

# Client code
def get_base_url(ip_address, port):
    """
    Constructs the base URL from the given IP address and port.
    """
    return f"http://{ip_address}:{port}"

def get_balance(base_url):
    """
    Sends GET request to /getbalance route and handles the server's response.
    """
    try:
        response = requests.get(f"{base_url}/getbalance", timeout=3)  # Set client timeout
        print(f"GET /getbalance - Status Code: {response.status_code}")
        
        # Check for 200 OK and print content
        if response.status_code == 200:
            print("Balance Page Content:", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.Timeout:
        # Handle client-side timeout
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions
        print(f"Request failed: {e}")

def get_logs(base_url):
    """
    Sends GET request to /getlogs route and prints the retrieved log data.
    """
    try:
        response = requests.get(f"{base_url}/getlogs")
        print(f"GET /getlogs - Status Code: {response.status_code}")
        
        # Check for 200 OK and display logs
        if response.status_code == 200:
            print("Logs:\n", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Execute client test code
if __name__ == "__main__":
    if len(sys.argv) != 3:
        # Display usage instructions
        print("Usage: python client.py <IP Address> <Port>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = sys.argv[2]
    base_url = get_base_url(ip_address, port)

    # testing /getbalance endpoint with multiple requests
    for _ in range(100):
        get_balance(base_url)
    
    # Retrieve and display logs from /getlogs endpoint
    get_logs(base_url)
