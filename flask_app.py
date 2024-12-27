from flask import Flask, request, jsonify
import random
from datetime import datetime
import joblib
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize Flask app
app = Flask(__name__)

# Load the trained fraud detection model (make sure to replace with your actual model)
model = joblib.load('fraud_model.pkl')  # Ensure you have a trained model saved as fraud_model.pkl

# Database setup (PostgreSQL)
DATABASE_URL = "postgresql://username:password@localhost:5432/fraud_detection_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Transaction model
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    sender_id = Column(String)
    receiver_id = Column(String)
    amount = Column(Float)
    fraud_label = Column(Integer)
    prediction_time = Column(DateTime, default=datetime.utcnow)

# Create the table (this can be done once)
Base.metadata.create_all(engine)

# Setup SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Simulate fraud detection (you can replace this with actual model logic)
def predict_fraud(transaction_data):
    # Simulate random fraud prediction
    fraud_probability = random.random()
    return 1 if fraud_probability > 0.8 else 0  # Fraudulent if probability > 0.8, else legitimate

# Save transaction data to the database
def save_transaction_to_db(transaction_data):
    transaction = Transaction(
        sender_id=transaction_data['sender_id'],
        receiver_id=transaction_data['receiver_id'],
        amount=transaction_data['amount'],
        fraud_label=transaction_data['fraud_label'],
        prediction_time=datetime.utcnow()
    )
    session.add(transaction)
    session.commit()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    transaction = data['transaction']
    
    # Perform fraud detection
    fraud_label = predict_fraud(transaction)
    
    # Add prediction result to the transaction
    transaction['Fraud_Label'] = fraud_label
    transaction['Prediction_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Optionally save the transaction to the database
    save_transaction_to_db(transaction)
    
    # Return the prediction result as JSON
    return jsonify(transaction)

@app.route('/')
def index():
    return "Mobile Money Fraud Detection API is running."

if __name__ == '__main__':
    app.run(debug=True)
