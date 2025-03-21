from flask import Flask, jsonify, send_file
import openai

app = Flask(__name__)

# Load API key
with open("OpenAI_API_Key.txt", "r") as f:
    openai.api_key = f.read().strip()

@app.route('/')
def serve_frontend():
    return send_file("index.html")  # Ensure index.html is in the same directory


@app.route('/api/get-text', methods=['GET'])
def get_text():
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Provide an advanced insight about relationships, consciousness, ethics, or living well in 3 sentences"}
            ]
        )

        bot_response = response.choices[0].message.content
        return jsonify({"output": bot_response})

    except Exception as e:
        print("Error:", str(e))  # Print error in terminal
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
