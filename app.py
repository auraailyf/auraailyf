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

def send_email(data):
    """Sends an email with the form submission data."""
    # Get your email credentials from environment variables by their NAME.
    sender_email = os.environ.get('EMAIL_SENDER')
    receiver_email = os.environ.get('EMAIL_RECEIVER')
    app_password = os.environ.get('EMAIL_APP_PASSWORD')

    # Check if all required email variables are set
    if not all([sender_email, receiver_email, app_password]):
        print("Error: Email credentials are not fully set in the environment variables.")
        return False

    # Create the email message content
    subject = f"New Contact Form Submission from {data.get('name')}"
    
    # Use HTML to format the email body nicely
    body = f"""
    <html>
    <head></head>
    <body style="font-family: sans-serif;">
        <h2 style="color: #333;">New Message from AuraAilyf Website</h2>
        <p><strong>Name:</strong> {data.get('name')}</p>
        <p><strong>Email:</strong> <a href="mailto:{data.get('email')}">{data.get('email')}</a></p>
        <p><strong>Company:</strong> {data.get('company', 'Not provided')}</p>
        <hr>
        <h3 style="color: #555;">Message:</h3>
        <p style="background-color: #f4f4f4; padding: 15px; border-radius: 5px;">
            {data.get('message')}
        </p>
    </body>
    </html>
    """

    # Set up the email object
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"AuraAilyf Website <{sender_email}>" # Display name for the sender
    message["To"] = receiver_email
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to Gmail's secure SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # Login using the sender email and the App Password
            server.login(sender_email, app_password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email notification sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/')
def home():
    """Renders the main index.html page."""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """Handles the form submission by sending an email."""
    data = request.get_json()
    # Basic validation
    if not data or not all(k in data for k in ['name', 'email', 'message']):
        return jsonify({'error': 'Missing required fields.'}), 400

    # Call the send_email function
    if send_email(data):
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 201
    else:
        # Send a generic error to the user if email fails
        return jsonify({'error': 'An internal server error occurred.'}), 500

if __name__ == '__main__':
    # Run the Flask development server (for local testing)
    # Set debug=False for production readiness, although Gunicorn ignores this
    app.run(debug=False)

