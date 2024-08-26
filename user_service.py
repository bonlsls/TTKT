from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for JWT
app.config['JWT_SECRET_KEY'] = 'abcabc'  # Change this to a secure key

# Initialize JWTManager
jwt = JWTManager(app)

# Your existing database setup and routes go here
# For example, user registration, login, etc.

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                       (username, hashed_password, email))
        user_id = cursor.lastrowid  # Get the auto-incremented user_id
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        access_token = create_access_token(identity={'user_id': user[0], 'username': user[1]})
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/authenticate', methods=['POST'])
@jwt_required()
def authenticate():
    current_user = get_jwt_identity()
    return jsonify({'user_id': current_user['user_id'], 'username': current_user['username']}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5005)
