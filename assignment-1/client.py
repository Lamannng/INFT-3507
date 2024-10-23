import requests

def send_requests():
    for _ in range(100):  # Adjust the number of requests as needed
        response = requests.get('http://localhost:8080/getbalance')
        print(f'GET /getbalance: {response.status_code} - {response.text}')

    response = requests.get('http://localhost:8080/getlogs')
    print(f'GET /getlogs: {response.status_code} - {response.json()}')

if __name__ == "__main__":
    send_requests()
