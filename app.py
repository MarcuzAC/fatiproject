from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pickle

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for session management. 
# In production, use an environment variable instead of hardcoding.
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Hardcoded credentials (use secure storage for production)
USER_CREDENTIALS = {
    'username': 'Fatima',
    'password': generate_password_hash('Fatima123')
}

# Load the machine learning model
try:
    with open('ml/model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    print("Model file not found. Please ensure 'ml/model.pkl' exists.")
    model = None

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('predict'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER_CREDENTIALS['username'] and check_password_hash(USER_CREDENTIALS['password'], password):
            session['logged_in'] = True
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            sex = 1 if request.form['sex'] == 'Male' else 0
            highbp = int(request.form['highbp'])
            highchol = int(request.form['highchol'])
            heart_rate = float(request.form['heart_rate'])
            previous_heart_problems = int(request.form['previous_heart_problems'])
            smoker = int(request.form['smoker'])
            stroke = int(request.form['stroke'])
            diabetes = int(request.form['diabetes'])
            physactivity = int(request.form['physactivity'])
            hvyalcoholconsump = int(request.form['hvyalcoholconsump'])
            anyhealthcare = int(request.form['anyhealthcare'])

            features = [[age, sex, highbp, highchol, heart_rate, previous_heart_problems, smoker,
                         stroke, diabetes, physactivity, hvyalcoholconsump, anyhealthcare]]

            if model:
                prediction1 = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1] * 100

                prediction = "Low Risk" if prediction1 == 0 and probability <= 30 else "High Risk"
                return render_template('prediction_form.html', prediction=prediction, probability=probability + 30)
            else:
                flash("Model not loaded. Please check the server configuration.", "error")
                return render_template('prediction_form.html')
        except ValueError:
            flash("Invalid input data. Please enter valid numbers.", "error")
            return render_template('prediction_form.html')

    return render_template('prediction_form.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
