from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for session security

# Sample user data for login
users = {
    "mathankumar": "mathankumar",
    "manoj": "manoj",
    "nithya":"nithya",
    "pavithra":"pavithra", 
    "saravanan":"saravanan"
}

def calculate_delivery_time_based_on_distance(new_delivery_distance):
    # Sample data
    data = [
        ['2023-01-01', '2023-01-05', 10],
        ['2023-01-02', '2023-01-06', 15],
        ['2023-01-03', '2023-01-07', 20],
        ['2023-01-04', '2023-01-08', 25],
        ['2023-01-05', '2023-01-10', 30]
    ]

    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=['GeneratedDate', 'ActualDeliveryDate', 'DeliveryDistance'])

    # Ensure the columns are correctly formatted
    df['GeneratedDate'] = pd.to_datetime(df['GeneratedDate'])
    df['ActualDeliveryDate'] = pd.to_datetime(df['ActualDeliveryDate'])

    # Calculate the delivery time (in days) for each delivery
    df['DeliveryTime'] = (df['ActualDeliveryDate'] - df['GeneratedDate']).dt.days

    # Prepare the data for linear regression
    X = df[['DeliveryDistance']]
    y = df['DeliveryTime']

    # Create and train the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the delivery time for the new delivery distance
    predicted_delivery_time = model.predict(np.array([[new_delivery_distance]]))[0]
    return predicted_delivery_time

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = request.json
    new_delivery_distance = float(data['delivery_distance'])

    predicted_delivery_time = calculate_delivery_time_based_on_distance(new_delivery_distance)
    
    return jsonify({'predicted_delivery_time': predicted_delivery_time})

if __name__ == '__main__':
    app.run(debug=True)
