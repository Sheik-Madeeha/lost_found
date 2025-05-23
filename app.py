from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Make sure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Madee@0107",  # Add your MySQL password here
    database="lost_found_db"  # Make sure this database exists
)
cursor = db.cursor()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Lost Item Form
@app.route('/report-lost')
def report_lost():
    return render_template('upload_lost.html')

# Found Item Form
@app.route('/report-found')
def report_found():
    return render_template('upload_found.html')

# Submit Lost Item
@app.route('/submit-lost', methods=['POST'])
def submit_lost():
    email = request.form['email']

    item_name = request.form['item_name']
    description = request.form['description']
    location = request.form['location']
    image = request.files['image']

    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        cursor.execute(
        "INSERT INTO lost_items (item_name, description, location, image_path, email) VALUES (%s, %s, %s, %s, %s)",
        (item_name, description, location, f"uploads/{filename}", email)
        )
    else:
        cursor.execute(
        "INSERT INTO lost_items (item_name, description, location, image_path, email) VALUES (%s, %s, %s, NULL, %s)",
        (item_name, description, location, email)
        )
        db.commit()

    return redirect(url_for('home'))

# Submit Found Item
@app.route('/submit-found', methods=['POST'])
def submit_found():
    email = request.form['email']
    item_name = request.form['item_name']
    description = request.form['description']
    location = request.form['location']
    image = request.files['image']

    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        cursor.execute(
        "INSERT INTO found_items (item_name, description, location, image_path, email) VALUES (%s, %s, %s, %s, %s)",
        (item_name, description, location, f"uploads/{filename}", email)
        )
        db.commit()
    
    return redirect(url_for('home'))

# Display Lost & Found Items
@app.route('/items')
def view_items():
    cursor.execute("SELECT * FROM lost_items ORDER BY id DESC")
    lost_items = cursor.fetchall()

    cursor.execute("SELECT * FROM found_items ORDER BY id DESC")
    found_items = cursor.fetchall()

    return render_template('get_items.html', lost_items=lost_items, found_items=found_items)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
