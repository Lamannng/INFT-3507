import json

# Load log entries from a JSON file (if they are stored that way)
with open('logfile.json', 'r') as file:
    logs = [json.loads(line) for line in file]

# Initialize counters
count_200 = 0
count_403 = 0
count_500 = 0
count_timeout = 0

# Count status codes
for entry in logs:
    status_code = entry['status_code']
    if status_code == 200:
        count_200 += 1
    elif status_code == 403:
        count_403 += 1
    elif status_code == 500:
        count_500 += 1
    elif status_code == "timeout":
        count_timeout += 1

# Total requests
total_requests = len(logs)

# Calculate percentages
percentage_200 = (count_200 / total_requests) * 100
percentage_403 = (count_403 / total_requests) * 100
percentage_500 = (count_500 / total_requests) * 100
percentage_timeout = (count_timeout / total_requests) * 100

# Print results
print(f"200: {percentage_200:.2f}%")
print(f"403: {percentage_403:.2f}%")
print(f"500: {percentage_500:.2f}%")
print(f"Timeout: {percentage_timeout:.2f}%")
