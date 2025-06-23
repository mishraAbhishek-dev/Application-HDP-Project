from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import pickle   
import numpy as np
import pandas as pd
import re
import joblib
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer




# Load the model (once)
model = joblib.load('heart_disease_model.pkl')

app = Flask(__name__)
app.secret_key = "fa21a4c5ca06fb085680495285b6ac9c"  # Change this to a secure secret key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = "./flask_sessions"
# app.config['SESSION_KEY_PREFIX'] = "flask_session:"

app.secret_key = "fa21a4c5ca06fb085680495285b6ac9c"
Session(app)    

CORS(app)



# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhi@1418",
    database="heart_disease_db"
)
cursor = db.cursor()

# Ensure users table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")
db.commit()




@app.route('/')
def home():
    return render_template('Landing.html')

@app.route('/register', methods=['POST'])
def register():
    
    if request.method == 'POST':
        name= request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(f"Name:{name}, Received email: {email}, password: {password}")

    # print("register:", name, email, password)
    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Insert new user into the database
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, hashed_password)
    cursor.execute(sql, values)
    db.commit()
    return redirect(url_for('home'))
    # return jsonify({"message": "User registered successfully",  "redirect": "/login"}), 201

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Received email: {email}, password: {password}")  # Debugging

        # Fetch user from the database
        cursor.execute("SELECT name, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        print("User fetched from DB:", user)  # Debugging

        if user and check_password_hash(user[1], password):  # Verify password
            print("Session before setting username:", dict(session))  # Debugging
            session['username'] = user[0]  # Store username in session
            
            print("Session after login:", dict(session))  # Debugging
            # return jsonify({"message": "Login successful", "redirect": "/prediction"})
            return redirect(url_for('predict_page'))
        else:
            print("Invalid login attempt")
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return redirect(url_for('home'))
    
    
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bhardwajabhi2800@gmail.com'  # Use your email here
app.config['MAIL_PASSWORD'] = 'gfav yvsl xytt ykvy'  # Use your email password here
app.config['MAIL_DEFAULT_SENDER'] = 'bhardwajabhi2800@gmail.com'  # Same as MAIL_USERNAME

mail = Mail(app)

@app.route('/test_email')
def test_email():
    msg = Message("Test Email",
                  recipients=["recipient_email@example.com"])  # Replace with a real email address
    msg.body = "This is a test email from Flask!"
    try:
        mail.send(msg)
        return "Test email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            # Generate a password reset link (use an actual token here)
            s = URLSafeTimedSerializer(app.secret_key)
            token = s.dumps(email)
            reset_link = url_for('reset_password', token=token, _external=True)  # Create reset link
            print("Generated reset link:", reset_link)

            print("Received token:", token)

            # Send the reset link via email
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Click on the link to reset your password: {reset_link}'
            mail.send(msg)

            return jsonify({"message": "Password reset link sent to your email!"}), 200
        else:
            return jsonify({"message": "Email not found"}), 404
    return render_template('ForgotPassword.html')  # Ensure this HTML exists



s = URLSafeTimedSerializer(app.secret_key)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Try to decode the token
        email = s.loads(token, max_age=86400)  # Token expires after 1 hour
        print("Decoded email from token:", email)
        if request.method == 'POST':
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if new_password != confirm_password:
                return jsonify({"message": "Passwords do not match!"}), 400

            # Reset the user's password (assuming you have a user model)
            else:
                return redirect(url_for('login'))  # Redirect to login after successful password reset

        return render_template('reset_password.html', token=token)

    except Exception as e:
        print(f"Error decoding token: {e}")
        return jsonify({"message": "The reset link is invalid or expired!"}), 400
    
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login')) 




@app.route('/prediction', methods=['GET'])
def predict_page():
    print(" Session in /prediction:", dict(session))  # Debugging statement
    
    print("Current session:", dict(session))

    if 'username' not in session:
        print(" Session is empty, redirecting to home")  # Debugging statement
        return redirect(url_for('home'))

    print(" User is logged in:", session['username'])  # Debugging statement
    return render_template('Prediction.html', username=session['username'])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from form
        username=session.get('username' )
        
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        cp = float(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        restecg = float(request.form['restecg'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])
        
        
        
        input_data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, exang, oldpeak, slope, ca, thal]],
                              columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                                       'restecg', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

        prediction = model.predict(input_data)
        prediction_prob = model.predict_proba(input_data)
        print("Input DataFrame:\n", input_data)
        print("Prediction Output:", prediction)
        print("Prediction Probabilities:", prediction_prob)

        print(request.form)

        result = "High chance of heart disease" if prediction[0] == 1 else "Low chance of heart disease"
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS heart_disease_predictions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            age FLOAT,
            sex FLOAT,
            cp FLOAT,
            trestbps FLOAT,
            chol FLOAT,
            fbs FLOAT,
            restecg FLOAT,
            exang FLOAT,
            oldpeak FLOAT,
            slope FLOAT,
            ca FLOAT,
            thal FLOAT,
            prediction VARCHAR(100),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        db.commit()

        
        insert_query = """INSERT INTO heart_disease_predictions 
                (username, age, sex, cp, trestbps, chol, fbs, restecg, exang, oldpeak, slope, ca, thal, prediction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        data = (username, age, sex, cp, trestbps, chol, fbs, restecg,
        exang, oldpeak, slope, ca, thal, result)


        cursor.execute(insert_query, data)
        db.commit()
        # Correct order of features
        
    
# Make sure you're checking prediction[0] correctly


        return render_template('Result.html', prediction=result, username=username, 
                       age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol,
                       fbs=fbs, restecg=restecg, exang=exang, oldpeak=oldpeak, 
                       slope=slope, ca=ca, thal=thal)


    except Exception as e:
        return f"Error: {str(e)}", 400
    
    



if __name__ == '__main__':
    app.run(debug=True)
