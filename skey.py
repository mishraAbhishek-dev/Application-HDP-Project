# # import secrets
# # print(secrets.token_hex(16)) 

# import mysql.connector

# try:
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Abhi@1418",  # Replace with your actual password
#         database="heart_disease_db"
#     )
#     cursor = db.cursor()
#     cursor.execute("SHOW TABLES;")  # Fetch tables
#     tables = cursor.fetchall()
#     print("✅ Database Connected Successfully!")
#     print("📌 Tables in Database:", tables)
    
# except mysql.connector.Error as err:
#     print("❌ Error Connecting to Database:", err)


# from flask import Flask, session
# from flask_session import Session

# app = Flask(__name__)

# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_FILE_DIR'] = "./flask_sessions"
# app.secret_key = "fa21a4c5ca06fb085680495285b6ac9c"

# Session(app)

# @app.route('/')
# def home():
#     session['test_key'] = "Test Value"
#     return f"Session Set! Go to /check"

# @app.route('/check')
# def check():
#     return f"Session Data: {dict(session)}"

# if __name__ == '__main__':
#     app.run(debug=True)

