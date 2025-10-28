import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
# Configure CORS to allow your frontend to communicate with the API
CORS(app, resources={r"/api/*": {"origins": "*"}})



@app.route('/')
def home():
    """Renders the main index.html page."""
    return render_template('index.html')



if __name__ == '__main__':
    # Run the Flask development server (for local testing)
    # Set debug=False for production readiness, although Gunicorn ignores this
    app.run(debug=False)

