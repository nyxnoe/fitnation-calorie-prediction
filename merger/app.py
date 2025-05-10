from flask import Flask, request, render_template, redirect, url_for, session
import numpy as np
import sqlite3
import pickle
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change in production!

model = pickle.load(open('pipeline.pkl', 'rb'))

# --- DB Initialization ---
def init_db():
    conn = sqlite3.connect('user_inputs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age REAL,
            height REAL,
            weight REAL,
            duration REAL,
            heart_rate REAL,
            body_temp REAL,
            predicted_calories REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            dob TEXT,
            mobile TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Home ---
@app.route('/')
def home():
    return render_template('home.html')

# --- Predictor Page ---
@app.route('/predictor')
def predictor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('predictor.html')

# --- Result Route ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        gender = request.form['gender']
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        duration = float(request.form['duration'])
        heart_rate = float(request.form['heart_rate'])
        body_temp = float(request.form['body_temp'])

        input_data = [[gender, age, height, weight, duration, heart_rate, body_temp]]
        prediction = model.predict(input_data)[0]

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            suggestion = "You're underweight. Focus on balanced nutrition."
        elif bmi < 25:
            suggestion = "You're in a healthy range. Keep it up!"
        elif bmi < 30:
            suggestion = "Slightly overweight. Try HIIT & adjust diet."
        else:
            suggestion = "Consider consulting a trainer. Focus on cardio & strength."

        conn = sqlite3.connect('user_inputs.db')
        c = conn.cursor()
        c.execute('''INSERT INTO inputs 
                     (gender, age, height, weight, duration, heart_rate, body_temp, predicted_calories)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (gender, age, height, weight, duration, heart_rate, body_temp, prediction))
        conn.commit()
        conn.close()

        return render_template('result.html', 
                               calories=round(prediction, 2), 
                               bmi=bmi, 
                               suggestion=suggestion)
    except Exception as e:
        print("❌ Error:", str(e))
        return f"Error: {str(e)}"

# --- Registration Route ---
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        dob = request.form['dob']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect('user_inputs.db')
        c = conn.cursor()

        # Check if email already exists
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing = c.fetchone()
        if existing:
            conn.close()
            return "⚠️ This email is already registered. Try logging in instead."

        # Insert new user
        c.execute('INSERT INTO users (name, age, gender, dob, mobile, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (name, age, gender, dob, mobile, email, hashed_pw))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    except Exception as e:
        print("❌ Registration error:", str(e))
        return f"Error: {str(e)}"


# --- Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('user_inputs.db')
        c = conn.cursor()
        c.execute('SELECT id, password FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('predictor'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# --- Run App ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
