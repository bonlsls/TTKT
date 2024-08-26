from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_email_notification(email, message):
    # Placeholder for actual email sending logic
    print(f"Sending email to {email}: {message}")

def send_sms_notification(phone, message):
    # Placeholder for actual SMS sending logic
    print(f"Sending SMS to {phone}: {message}")

@app.route('/notify', methods=['POST'])
def notify():
    notification_data = request.json
    order_id = notification_data.get('order_id')
    customer_email = notification_data.get('email')
    customer_phone = notification_data.get('phone')
    message = notification_data.get('message')

    # 1. Send Notifications
    if customer_email:
        send_email_notification(customer_email, message)
    
    if customer_phone:
        send_sms_notification(customer_phone, message)

    # 2. Publish Notification to Kafka
    producer.send('notification-topic', {
        'order_id': order_id,
        'email': customer_email,
        'phone': customer_phone,
        'message': message
    })

    return jsonify({'status': 'notification_sent', 'order_id': order_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
