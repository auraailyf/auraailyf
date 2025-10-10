import os
import sys
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Define the name of our CSV file
CSV_FILE = 'submissions.csv'

def write_to_csv(data):
    """Appends form data to a CSV file."""
    # Check if the file already exists to decide whether to write headers
    file_exists = os.path.isfile(CSV_FILE)
    
    try:
        # 'a' means 'append' mode. newline='' prevents extra blank rows.
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            # Define the order of columns
            fieldnames = ['name', 'email', 'company', 'message', 'submitted_at']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # If the file is new, write the header row first
            if not file_exists:
                writer.writeheader()

            # Add the current timestamp to the data
            data_to_write = {
                'name': data.get('name'),
                'email': data.get('email'),
                'company': data.get('company'),
                'message': data.get('message'),
                'submitted_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Write the new row of data
            writer.writerow(data_to_write)
        print(f"Successfully wrote data to {CSV_FILE}")
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False

@app.route('/')
def home():
    """Renders the main index.html page."""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """Saves form submissions to a CSV file."""
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'email', 'message']):
        return jsonify({'error': 'Missing required fields.'}), 400

    # Call our new function to write the data to the CSV
    if write_to_csv(data):
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 201
    else:
        return jsonify({'error': 'An internal server error occurred while saving data.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

