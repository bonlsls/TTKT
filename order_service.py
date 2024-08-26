from flask import Flask, request, jsonify
from kafka import KafkaProducer
import requests
import json

app = Flask(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulated in-memory order database
order_db = {}

@app.route('/create_order', methods=['POST'])
def create_order():
    order_data = request.json
    customer_id = order_data['customer_id']
    product_id = order_data['product_id']
    quantity = order_data['quantity']
    address = order_data['address']

    # 1. User Authentication
    auth_response = requests.post('http://user_service:5005/authenticate', json={'customer_id': customer_id})
    if auth_response.status_code != 200 or auth_response.json().get('status') != 'authenticated':
        return jsonify({'status': 'failed', 'message': 'User authentication failed'}), 400

    # 2. Check Stock Availability
    stock_response = requests.post('http://stock_service:5002/check_stock', json={'product_id': product_id, 'quantity': quantity})
    if stock_response.status_code != 200 or stock_response.json().get('status') != 'in_stock':
        return jsonify({'status': 'failed', 'message': 'Product out of stock'}), 400

    # 3. Create Order (assuming order ID is auto-generated)
    order_id = len(order_db) + 1
    order_db[order_id] = {
        'customer_id': customer_id,
        'product_id': product_id,
        'quantity': quantity,
        'address': address,
        'status': 'pending'
    }

    # 4. Send Payment Request
    payment_response = requests.post('http://payment_service:5003/process_payment', json={'order_id': order_id, 'amount': 100})  # assuming amount is 100 for simplicity
    if payment_response.status_code != 200 or payment_response.json().get('status') != 'payment_successful':
        return jsonify({'status': 'failed', 'message': 'Payment failed'}), 400

    # 5. Publish Order Information to Kafka
    producer.send('order-topic', {'order_id': order_id, 'status': 'order_created'})

    # 6. Send Notification
    notification_response = requests.post('http://notification_service:5004/notify', json={'order_id': order_id, 'message': 'Your order has been placed successfully!'})
    if notification_response.status_code != 200:
        return jsonify({'status': 'failed', 'message': 'Notification failed'}), 500

    # Update order status after successful payment and notification
    order_db[order_id]['status'] = 'confirmed'

    return jsonify({'status': 'success', 'order_id': order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
