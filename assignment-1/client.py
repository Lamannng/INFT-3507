import requests

# Base URL of the server (update host and port as necessary)
base_url = 'http://localhost:8080'

def get_balance():
    """
    Sends GET request to /getbalance route and handles responses.
    """
    try:
        response = requests.get(f"{base_url}/getbalance", timeout=3)  # Adding timeout for client as well
        print(f"GET /getbalance - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Balance Page Content:", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def get_logs():
    """
    Sends GET request to /getlogs route and displays log data.
    """
    try:
        response = requests.get(f"{base_url}/getlogs")
        print(f"GET /getlogs - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Logs:\n", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Test functions by calling /getbalance multiple times
if __name__ == "__main__":
    for _ in range(100):  # Calling /getbalance multiple times
        get_balance()
    
    get_logs()  # Retrieve and display logs
