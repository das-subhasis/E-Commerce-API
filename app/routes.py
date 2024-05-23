from flask import Blueprint, request, jsonify
from .extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password']
    }
    result = mongo.db.users.insert_one(user)
    return jsonify({"message": "User created", "user_id": str(result.inserted_id)}), 201

@api.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = {
        'name': data['name'],
        'description': data.get('description'),
        'price': data['price'],
        'quantity': data['quantity']
    }
    result = mongo.db.products.insert_one(product)
    return jsonify({"message": "Product created", "product_id": str(result.inserted_id)}), 201

@api.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    result = [{"id": str(p["_id"]), "name": p["name"], "description": p.get("description"), "price": p["price"], "quantity": p["quantity"]} for p in products]
    return jsonify(result), 200

@api.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    product_orders = data['products']

    total_price = 0
    for product_order in product_orders:
        product = mongo.db.products.find_one({"_id": ObjectId(product_order['product_id'])})
        total_price += product['price'] * product_order['quantity']

    order = {
        'user_id': user_id,
        'products': product_orders,
        'total_price': total_price,
        'timestamp': datetime.utcnow()
    }
    result = mongo.db.orders.insert_one(order)
    return jsonify({"message": "Order created", "order_id": str(result.inserted_id)}), 201

@api.route('/orders', methods=['GET'])
def get_orders():
    orders = mongo.db.orders.find()
    result = [{
        "id": str(o["_id"]),
        "user_id": o["user_id"],
        "total_price": o["total_price"],
        "timestamp": o["timestamp"],
        "products": o["products"]
    } for o in orders]
    return jsonify(result), 200
