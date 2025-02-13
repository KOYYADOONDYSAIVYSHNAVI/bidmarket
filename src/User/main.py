from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes.user_routes import user_bp
from db import db, mongo
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/userdb' if not os.environ.get('MYSQL_URI') else os.environ.get('MYSQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Use an environment variable in production
app.config['MONGO_URI'] = 'mongodb://localhost:27017' if not os.environ.get('MONGODB_URI') else os.environ.get('MONGODB_URI')

# Initialize extensions
#db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api/users")
db.init_app(app)
mongo.init_app(app)


# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    return {"message": str(e)}, 500

if __name__ == "__main__":
    # Initialize the database if not already created
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 5001), debug=True)
