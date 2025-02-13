import os

from flask import Flask
from flask_cors import CORS

from views import auction_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(auction_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 8095), debug=True)
