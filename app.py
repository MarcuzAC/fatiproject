from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pickle

# Initialize Flask app (no need to specify template_folder if it's named 'templates')
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'

# Hardcoded credentials (use a secure storage method or database for production)
USER_CREDENTIALS = {
    'username': 'Fatima',
    'password': generate_password_hash('Fatima123')  # Store password as a hash
}

# Load the machine learning model
with open('ml/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('predict'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        if username == USER_CREDENTIALS['username'] and check_password_hash(USER_CREDENTIALS['password'], password):
            session['logged_in'] = True
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Check if user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
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

        # Create feature vector for model
        features = [[age, sex, highbp, highchol, heart_rate, previous_heart_problems, smoker, stroke, diabetes, physactivity, hvyalcoholconsump, anyhealthcare]]

        # Predict using the model
        prediction1 = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1] * 100  # Assuming binary classifier

        # Determine risk level
        prediction = "Low Risk" if prediction1 == 0 and probability <= 30 else "High Risk"

        # Pass prediction and adjusted probability to the template
        return render_template('prediction_form.html', prediction=prediction, probability=probability + 30)

    return render_template('prediction_form.html')

@app.route('/logout')
def logout():
    # Clear session and redirect to login
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the app in debug mode (remove debug=True for production)
    app.run(debug=True)
