from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def notify():
    event = request.get_json()
    message = {
        "status": "notified",
        "function": "notifier",
        "event_type": event.get("event_type"),
        "file_name": event.get("file_name"),
        "timestamp": datetime.now().isoformat()
    }
    print("NOTIFICATION:", message, flush=True)
    return jsonify(message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
