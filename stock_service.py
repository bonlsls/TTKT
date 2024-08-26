from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Simulated in-memory stock database
stock_db = {
    'product_1': 10,
    'product_2': 5,
    'product_3': 15
}

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/check_stock', methods=['POST'])
def check_stock():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    if stock_db.get(product_id, 0) >= quantity:
        response = {'status': 'in_stock'}
    else:
        response = {'status': 'out_of_stock'}

    # Send stock check result to Kafka for asynchronous processing
    producer.send('stock-check-results', {'product_id': product_id, 'status': response['status']})

    return jsonify(response)


@app.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    if stock_db.get(product_id, 0) >= quantity:
        stock_db[product_id] -= quantity
        response = {'status': 'stock_updated'}

        # Publish stock update to Kafka
        producer.send('stock-updates', {'product_id': product_id, 'new_quantity': stock_db[product_id]})
    else:
        response = {'status': 'out_of_stock'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
