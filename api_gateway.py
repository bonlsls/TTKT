from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mapping services to their respective URLs
services = {
    'order': 'http://localhost:5001',
    'payment': 'http://localhost:5003',
    'stock': 'http://localhost:5002',
    'notification': 'http://localhost:5004',
    'user':'http://localhost:5005'
}

def forward_request(service_url):
    try:
        response = requests.request(
            method=request.method,
            url=service_url + request.path,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
        
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Routing to Order Service
@app.route('/api/order', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/order/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def order_service(path):
    return forward_request(services['order'])

# Routing to Payment Service
@app.route('/api/payment', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/payment/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def payment_service(path):
    return forward_request(services['payment'])

# Routing to Stock Service
@app.route('/api/stock', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/stock/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def stock_service(path):
    return forward_request(services['stock'])

# Routing to Notification Service
@app.route('/api/notify', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/notify/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def notification_service(path):
    return forward_request(services['notification'])

# Routing to User Service
@app.route('/api/user', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/user/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_service(path):
    return forward_request(services['user'])

# Default route to check if the API Gateway is up
@app.route('/')
def index():
    return "API Gateway is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
