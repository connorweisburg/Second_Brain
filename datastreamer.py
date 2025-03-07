import time

logs = []  # List to store log messages

def start_datastream():
    global logs
    clear_logs()  # Clear previous logs before starting the count
    count = 0  # Start counting from 0
    # Simulate counting from 1 to 100
    while count < 100:
        count += 1
        logs.append(f"Count: {count}")  # Append current count to logs
        time.sleep(1)  # Wait for 1 second

    logs.append("✅ Counting completed.")

def get_logs():
    global logs
    return logs

def clear_logs():
    global logs
    logs = []  # Clear the logs before starting new stream
