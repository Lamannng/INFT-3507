import requests
import time
import random

# Set the base URL for your server (update IP and port as needed)
base_url = 'http://localhost:8080'

def get_balance():
    """Sends a GET request to the /getbalance route and logs the response."""
    try:
        response = requests.get(f"{base_url}/getbalance", timeout=2)
        print(f"GET /getbalance - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.Timeout:
        print("GET /getbalance - Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_logs():
    """Sends a GET request to the /getlogs route and logs the response."""
    try:
        response = requests.get(f"{base_url}/getlogs")
        print(f"GET /getlogs - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Logs:", response.json())
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Simulate calling /getbalance multiple times
    for _ in range(10):
        get_balance()
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between requests

    # Retrieve logs once
    get_logs()
