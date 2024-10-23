import requests #to make http requests 
import time        #to add delays

# Define the server URL. This should match where your server is running.
server_url = 'http://localhost:8080'

def get_balance():
    """
    Function to send a GET request to the /getbalance route.
    It prints the status code and response content for each request.
    """
    try:
        #sending request to get balance endpoint
        response = requests.get(f'{server_url}/getbalance')
        
        # Printing status code and response content to the console
        print(f'GET /getbalance: {response.status_code} - {response.text}')
    except Exception as e:
        # Handle any exceptions that occur during the request
        print(f'Error fetching balance: {e}')
def get_logs():
    """
    Function to send a GET request to the /getlogs route.
    It prints the status code and the retrieved log data in JSON format.
    """
    try:
        # Send a GET request to the /getlogs endpoint
        response = requests.get(f'{server_url}/getlogs')
        
        # Print the status code and log data to the console
        print(f'GET /getlogs: {response.status_code} - {response.json()}')
    except Exception as e:
        # Handle any exceptions that occur during the request
        print(f'Error fetching logs: {e}')

if __name__ == "__main__":
    # Main execution block of the script
    for _ in range(10):  # Loop to call the get_balance function 10 times
        get_balance()     # Call the function to fetch balance data
        time.sleep(1)     # Wait for 1 second between calls to avoid overwhelming the server

    get_logs()  # After the balance requests, fetch and print the logs
