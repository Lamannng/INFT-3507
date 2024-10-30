import json  # Import the JSON module for parsing JSON data

# Load log entries from a JSON file (if they are stored that way)
with open('logfile.json', 'r') as file:
    # Read each line in the file, parse it as JSON, and store it in a list called 'logs'
    logs = [json.loads(line) for line in file]

# Initialize counters for each status code
count_200 = 0       # Counter for successful requests (HTTP 200)
count_403 = 0       # Counter for forbidden requests (HTTP 403)
count_500 = 0       # Counter for server errors (HTTP 500)
count_timeout = 0   # Counter for timeout occurrences

# Count status codes in the logs
for entry in logs:
    status_code = entry['status_code']  # Extract the status code from each log entry
    if status_code == 200:
        count_200 += 1  # Increment the counter for HTTP 200 responses
    elif status_code == 403:
        count_403 += 1  # Increment the counter for HTTP 403 responses
    elif status_code == 500:
        count_500 += 1  # Increment the counter for HTTP 500 responses
    elif status_code == "timeout":
        count_timeout += 1  # Increment the counter for timeout occurrences

# Calculate the total number of requests logged
total_requests = len(logs)

# Calculate percentages of each status code
percentage_200 = (count_200 / total_requests) * 100           # Percentage of successful requests
percentage_403 = (count_403 / total_requests) * 100           # Percentage of forbidden requests
percentage_500 = (count_500 / total_requests) * 100           # Percentage of server errors
percentage_timeout = (count_timeout / total_requests) * 100    # Percentage of timeout occurrences

# Print the results with two decimal places for better readability
print(f"200: {percentage_200:.2f}%")         # Print the percentage of HTTP 200 responses
print(f"403: {percentage_403:.2f}%")         # Print the percentage of HTTP 403 responses
print(f"500: {percentage_500:.2f}%")         # Print the percentage of HTTP 500 responses
print(f"Timeout: {percentage_timeout:.2f}%") # Print the percentage of timeout occurrences
