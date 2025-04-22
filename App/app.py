from flask import Flask
from flask_cors import CORS
import os
from logic import init_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Secure session

CORS(app)

# Create DB if it doesn't exist
if not os.path.exists('mental_wellness.db'):
    init_db()

# Import routes (must be after app is defined)
from routes import *

# For local clinical testing (Number 9)
if __name__ == "__main__":
    app.run(debug=True)
