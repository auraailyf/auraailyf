import os
import sys # <-- Import sys
import psycopg2
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

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_table():
    """Creates the contact_submissions table."""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contact_submissions (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    company VARCHAR(255),
                    message TEXT NOT NULL,
                    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cur.close()
            print("Table 'contact_submissions' is ready.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

@app.route('/')
def home():
    """Renders the main index.html page."""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """Saves form submissions to the database."""
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'email', 'message']):
        return jsonify({'error': 'Missing required fields.'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed.'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contact_submissions (name, email, company, message) VALUES (%s, %s, %s, %s)",
            (data['name'], data['email'], data.get('company'), data['message'])
        )
        conn.commit()
        cur.close()
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 201
    except Exception as e:
        print(f"Error inserting data: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500
    finally:
        conn.close()

# --- NEW BLOCK FOR RUNNING COMMANDS ---
if __name__ == '__main__':
    # Check if a command-line argument was passed
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        create_table()
    else:
        # This will run when you start the server normally
        app.run(debug=False)