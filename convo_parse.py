import json
from datetime import datetime

# Load your OpenAI memory bank JSON
with open("conversations.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # This is a list of conversations

# Store interests (user questions) and knowledge (AI responses)
interests = []  # (timestamp, question)
knowledge = []  # (timestamp, AI response)

# Loop through each conversation in the JSON
for conversation in data:  
    if "mapping" in conversation:
        for message_id, message_data in conversation["mapping"].items():
            if "message" in message_data and message_data["message"]:  
                message = message_data["message"]
                
                # Extract timestamp
                timestamp = message.get("create_time", None)
                if timestamp:
                    timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                # Extract user messages (things you like)
                if message["author"]["role"] == "user":
                    question_text = message["content"]["parts"][0] if "parts" in message["content"] else ""
                    interests.append((timestamp, question_text))
                
                # Extract AI responses (things you know)
                elif message["author"]["role"] == "assistant":
                    response_text = message["content"]["parts"][0] if "parts" in message["content"] else ""
                    knowledge.append((timestamp, response_text))

# Save user inputs with timestamps
with open("user_interests_with_timestamps.txt", "w", encoding="utf-8") as f:
    for timestamp, question in interests:
        f.write(f"{timestamp} | {question}\n")

# Save AI responses with timestamps
with open("user_knowledge_with_timestamps.txt", "w", encoding="utf-8") as f:
    for timestamp, response in knowledge:
        f.write(f"{timestamp} | {response}\n")

print(f"✅ Extracted {len(interests)} user questions and {len(knowledge)} AI responses successfully!")
