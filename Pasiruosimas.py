from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='templates')

# Connect to SQLite database and create table if not exists
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL
                )''')
conn.commit()

# Function to get a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to get all notes from the database
def get_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return notes

# Function to add a new note to the database
def add_note(note_content):
    conn = get_db_connection()
    conn.execute('INSERT INTO notes (content) VALUES (?)', (note_content,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        add_note(note)  # Add note to database
        return redirect(url_for('index'))  # Redirect to avoid resubmission on page refresh
    all_notes = get_notes()  # Get all notes from the database
    last_3_notes = all_notes[-3:]  # Get the last 3 notes
    return render_template('index.html', last_3_notes=last_3_notes)

@app.route('/view_all')
def view_all():
    all_notes = get_notes()  # Get all notes from the database
    return render_template('notes.html', all_notes=all_notes)

if __name__ == '__main__':
    app.run(debug=True)
