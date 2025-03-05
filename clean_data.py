import re

# Load raw data
with open("user_interests_with_timestamps.txt", "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

# Processed output
cleaned_requests = []
current_request = ""

for line in raw_lines:
    # Match timestamp format (YYYY-MM-DD HH:MM:SS | )
    timestamp_match = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| ", line)

    if timestamp_match:
        # If there's an existing request, save it before starting a new one
        if current_request.strip():
            cleaned_requests.append(current_request.strip())
        # Start a new request (remove timestamp)
        current_request = line[len(timestamp_match.group()):].strip()
    else:
        # Append to the current request (remove extra spaces)
        current_request += " " + line.strip()

# Append the last request
if current_request.strip():
    cleaned_requests.append(current_request.strip())

# Save the cleaned output
with open("cleaned_user_requests.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(cleaned_requests))

print(f"✅ Processed {len(cleaned_requests)} user requests into a clean dataset!")
