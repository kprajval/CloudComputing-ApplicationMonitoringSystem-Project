from flask import Flask, jsonify, request
import random, time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Monitoring API"})

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "User logged in", "status": 200})

@app.route('/products', methods=['GET'])
def get_products():
    products = ["Laptop", "Phone", "Monitor", "Keyboard"]
    return jsonify({"products": products, "count": len(products)})

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify({"product_id": id, "name": f"Product-{id}"})

@app.route('/order', methods=['POST'])
def place_order():
    order_id = random.randint(1000, 9999)
    return jsonify({"order_id": order_id, "status": "Order placed"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "timestamp": time.time()})

@app.route('/error', methods=['GET'])
def generate_error():
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
