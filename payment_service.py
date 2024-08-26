from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import random

app = Flask(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_data = request.json
    order_id = payment_data['order_id']
    card_number = payment_data.get('card_number')
    expiry_date = payment_data.get('expiry_date')
    cvv = payment_data.get('cvv')
    amount = payment_data.get('amount')

    # 1. Validate Payment Information
    if not all([card_number, expiry_date, cvv, amount]):
        return jsonify({'status': 'failed', 'message': 'Invalid payment information'}), 400

    # 2. Simulate Payment Processing (In real scenarios, integrate with a payment gateway)
    # Here, we're randomly determining success or failure to simulate a payment process.
    payment_successful = random.choice([True, False])

    if payment_successful:
        transaction_status = 'payment_successful'
    else:
        transaction_status = 'payment_failed'

    # 3. Publish Transaction Result to Kafka
    producer.send('payment-transactions', {
        'order_id': order_id,
        'status': transaction_status,
        'amount': amount
    })

    # 4. Return Payment Result to Order Service
    return jsonify({'status': transaction_status, 'order_id': order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
