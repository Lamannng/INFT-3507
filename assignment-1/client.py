import sys  # Module to access command-line arguments
import requests  # Library for making HTTP requests
import json  # Module for handling JSON data
import time  # Module for time-related functions

def main(host, port):
    """
    Main function to execute the client application that interacts with the server.

    Args:
        host (str): The IP address or hostname of the server.
        port (str): The port number on which the server is listening.
    """
    # Construct URLs for the /getbalance and /getlogs endpoints
    getbalance_url = f"http://{host}:{port}/getbalance"
    getlogs_url = f"http://{host}:{port}/getlogs"

    # Counters for tracking successful and failed requests
    successful_requests = 0
    failed_requests = 0
    total_requests = 100  # Total number of requests to send

    # Making 100 requests to /getbalance to generate logs
    for i in range(total_requests):
        try:
            # sending a GET request to the /getbalance endpoint with a timeout of 10 seconds
            response = requests.get(getbalance_url, timeout=10)
            # checking the response status code
            if response.status_code == 200:
                successful_requests += 1  # Increment the success counter
                print(f"Request {i + 1}: Balance retrieved successfully.")
            elif response.status_code in [403, 500]:
                failed_requests += 1  # Increment the failure counter for specific error codes
                print(f"Request {i + 1}: Error {response.status_code}.")
            else:
                failed_requests += 1  # Increment the failure counter for unexpected responses
                print(f"Request {i + 1}: Unexpected response:", response.status_code)
        except requests.exceptions.Timeout:
            failed_requests += 1  # Increment the failure counter on timeout
            print(f"Request {i + 1}: Request timed out. Retrying...")
            time.sleep(1)  # Wait a second before retrying the request
            continue  # Skip the increment and retry the request
        except requests.exceptions.RequestException as e:
            failed_requests += 1  # Increment the failure counter on general request exceptions
            print(f"Request {i + 1}: Request error: {e}")

        time.sleep(0.5)  # Optional: pause between requests to avoid overwhelming the server

    # Print a summary of successful and failed requests
    print(f"\nSummary: Successful Requests: {successful_requests}, Failed Requests: {failed_requests}")

    # Fetch logs from /getlogs endpoint
    try:
        # Send a GET request to the /getlogs endpoint with a timeout of 10 seconds
        response = requests.get(getlogs_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)

        # Read response line by line and parse each line as JSON
        logs = response.text.splitlines()  # Split the response into separate lines
        print("Logs retrieved from server:")
        for log_line in logs:
            try:
                log_entry = json.loads(log_line)  # Parse each line as a JSON object
                print(log_entry)  # Print the parsed log entry
            except json.JSONDecodeError:
                print("Warning: Skipping a line due to JSON decoding error.")  # Handle JSON parsing errors

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting logs: {e}")  # Handle exceptions when fetching logs

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")  # Print usage instructions
        sys.exit(1)  # Exit the program with an error code

    host = sys.argv[1]  # Get the host from the command-line arguments
    port = sys.argv[2]  # Get the port from the command-line arguments
    main(host, port)  # Call the main function with the provided host and port
