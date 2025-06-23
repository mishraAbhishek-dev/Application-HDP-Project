# Heart Disease Prediction Project

This web application helps predict the likelihood of heart disease using machine learning algorithms based on user-provided medical parameters. The project includes a user-friendly frontend and a Flask backend connected to a trained model and a MySQL database.

---

## 🚀 Features

- 🔐 User Registration & Login System
- 🔁 Forgot & Reset Password via Email
- 📊 Input form to enter key health parameters
- 🤖 ML Model prediction with result display
- 🧾 History stored in database (MySQL)
- 🎨 Attractive UI with Bootstrap

---

## 🛠️ Tech Stack

### Frontend:
- HTML5, CSS3
- Bootstrap 5

### Backend:
- Python 3
- Flask Framework
- Flask-Mail, Flask-Session
- MySQL (with `mysql-connector-python`)

### ML Model:
- scikit-learn
- joblib / pickle for model loading

---

## 📁 Project Structure

MajorProject/
│
├── app.py # Main Flask app
├── heart_disease_model.pkl # Trained ML model
├── templates/ # HTML files
│ ├── Landing.html
│ ├── Prediction.html
│ ├── Forgotpassword.html
│ └── Result.html (optional)
├── static/ # Static files (images, CSS)
└── requirements.txt # Python dependencies (recommended to add)


---

## 🔧 How to Run the Project Locally

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/Application-HDP-Project.git
cd Application-HDP-Project

Set up Virtual Environment (Optional but Recommended)

python -m venv venv
venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Start MySQL Database

Ensure your database heart_disease_db is created

Update DB credentials in app.py if needed

Run the App

python app.py
Visit in Browser
http://127.0.0.1:5000/