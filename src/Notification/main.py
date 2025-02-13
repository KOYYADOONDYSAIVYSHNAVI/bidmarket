from flask import Flask
from app.consumers import listen_for_events

app = Flask(__name__)

@app.route('/')
def home():
    return "Notification Service is running!"

if __name__ == "__main__":
    # Start RabbitMQ consumer in a separate thread
    from threading import Thread
    thread = Thread(target=listen_for_events)
    thread.start()

    app.run(debug=True, host="0.0.0.0", port=5000)
