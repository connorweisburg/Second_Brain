from flask import Flask, jsonify, request, send_file
import openai
import re

app = Flask(__name__)

# Load API key
with open("OpenAI_API_Key.txt", "r") as f:
    openai.api_key = f.read().strip()

@app.route('/')
def serve_frontend():
    return send_file("index.html")  # Ensure index.html is in the same directory

last_response = None  # Store only the last response

@app.route('/api/get-text', methods=['GET'])
def get_text():
    global last_response

    try:
        user_topic = request.args.get('topic', '')  # Get user input if provided
        messages = []

        if user_topic:  
            print(f"User provided a topic: {user_topic}")  # Log user input

            # Case 3: User provides a new topic, combining it with the last response
            if last_response:
                print(f"Last response exists: {last_response}")  # Log last response

                sentences = re.split(r'(?<=[.!?]) +', last_response.strip())
                last_sentence = sentences[-1] if sentences else ""

                print(f"Extracted last sentence: {last_sentence}")  # Log last sentence

                prompt = (f"Give me 3 sentences that flow out of \"{last_sentence}\" and transition into this topic: \"{user_topic}\"")
            else:
                print("No last response found. Generating a new insight.")  # Log new topic generation
                prompt = f"Generate an advanced insight about \"{user_topic}\" in 3 sentences"
            
            messages.append({"role": "system", "content": prompt})
            print(f"Final prompt: {prompt}")  # Log final prompt

        elif last_response:  
            # Case 2: Feed last response into itself
            sentences = re.split(r'(?<=[.!?]) +', last_response.strip())
            last_sentence = sentences[-1] if sentences else ""
            prompt = f"Give me three sentences that flow out of this one: \"{last_sentence}\" and take it somewhere new."
            messages.append({"role": "system", "content": prompt})

        else:  
            # Case 1: Basic request
            prompt = "Provide an advanced insight about living well in 3 sentences."
            messages.append({"role": "system", "content": prompt})

        # Request to OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_response = response.choices[0].message.content
        last_response = bot_response  # Update stored response

        return jsonify({"output": bot_response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
