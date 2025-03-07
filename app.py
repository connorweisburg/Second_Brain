from flask import Flask, jsonify
import subprocess
import threading
import time
from datastreamer import start_datastream, get_logs, clear_logs

app = Flask(__name__)

def run_clustering():
    global logs
    clear_logs()  # Clear previous logs before starting a new run
    start_datastream()  # Start generating log messages

@app.route('/')
def serve_frontend():
    return open("index.html").read()

@app.route('/api/run-clustering', methods=['POST'])
def run_clustering_api():
    thread = threading.Thread(target=run_clustering)  # Run in a separate thread
    thread.start()
    return jsonify({"status": "started"})

@app.route('/api/get-logs')
def get_logs_api():
    logs = get_logs()
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
