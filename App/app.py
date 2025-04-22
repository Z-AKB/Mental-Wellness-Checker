from flask import Flask
from flask_cors import CORS
import os
from logic import init_db
from routes import app_routes  # Import the blueprint

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Secure session

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Initialize the database if it doesn't exist
if not os.path.exists('mental_wellness.db'):
    init_db()

# Register the blueprint from routes.py
app.register_blueprint(app_routes)

# Run the application for local clinical testing
if __name__ == "__main__":
    app.run(debug=True)
