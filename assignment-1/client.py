import requests

# Set the base URL for your server
base_url = 'http://localhost:8080'  # Using localhost as specified

# Function to get balance
def get_balance():
    """
    Sends a GET request to the /getbalance route and logs the response.
    """
    try:
        response = requests.get(f"{base_url}/getbalance")
        print(f"GET /getbalance - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.text)
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Function to get logs
def get_logs():
    """
    Sends a GET request to the /getlogs route and logs the response.
    """
    try:
        response = requests.get(f"{base_url}/getlogs")
        print(f"GET /getlogs - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Logs:", response.json())
        else:
            print("Error Response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Test the functions by calling them multiple times
if __name__ == "__main__":
    for _ in range(10):  # Call get_balance multiple times
        get_balance()
    
    get_logs()  # Call get_logs once
