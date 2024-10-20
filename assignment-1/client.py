import requests

# Test the /getbalance and /getlogs routes
def test_server(server_ip, server_port):
    for _ in range(10):
        try:
            response = requests.get(f'http://{server_ip}:{server_port}/getbalance')
            print(f"/getbalance returned: {response.status_code}")
        except Exception as e:
            print(f"Error during /getbalance: {e}")
    
    # Fetch and display logs
    try:
        logs_response = requests.get(f'http://{server_ip}:{server_port}/getlogs')
        logs = logs_response.json()
        print("\nLogs from server:")
        for log in logs:
            print(log)
    except Exception as e:
        print(f"Error during /getlogs: {e}")

if __name__ == "__main__":
    test_server('localhost', 8080)
