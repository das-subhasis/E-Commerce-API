from flask import Blueprint, request, jsonify
from .extensions import mongo, validate_api_key
from .models import User, Products,  Orders

# Loading blueprint for our api
api = Blueprint('api', __name__)


@api.route('/register', methods=['POST'])
def register_users():
    try:
        api_key = request.args.get('api_key')

        # validate API key
        if not validate_api_key(api_key=api_key):
            return jsonify({"error": "Invalid API key"}), 403

        # extract user data from request
        user_data = request.json
        user_exists = mongo.db.users.find_one({'email': user_data['email']})
        # check if user already exists
        if user_exists:
            return jsonify({"error": "User already exists"}), 409

        # create new user and save to database
        new_user = User(**user_data)
        result = new_user.save()
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/users', methods=['GET'])
def get_users():
    try:
        # validate API key
        api_key = request.args.get('api_key')
        if not validate_api_key(api_key=api_key):
            return jsonify({"error": "Invalid API key"}), 403

        # Find all users in the database
        users_data = list(mongo.db.users.find({}, {'password': 0}))

        # Check if user database is empty or not
        if users_data:
            return jsonify(users_data), 200
        else:
            return jsonify({"message": "No users found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        # validate API key
        api_key = request.args.get('api_key')
        if not validate_api_key(api_key=api_key):
            return jsonify({"error": "Invalid API key"}), 403

        # Find user with specified id
        user_data = mongo.db.users.find_one({"_id": user_id}, {'password': 0})
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/products', methods=['GET', 'POST'])
def get_products():
    try:
        # validate API key
        api_key = request.args.get('api_key')
        if not validate_api_key(api_key=api_key):
            return jsonify({"error": "Invalid API key"}), 403

        if request.method == 'GET':

            # Get product name from request parameters
            product_name = request.args.get('product_name')
            if product_name:
                # Find the specified product
                product_data = mongo.db.products.find_one(
                    {"product_name": product_name})

                if product_data:
                    return jsonify(product_data), 200
                else:
                    return jsonify({"message": "Product not found"}), 404
            else:
                products_data = list(mongo.db.products.find({}, {'_id': 0}))
                if products_data:
                    return jsonify(products_data), 200
                else:
                    return jsonify({"message": "No products found"}), 404

        elif request.method == 'POST':

            # Extract product data from request
            product_data = request.json

            # Create new product and save to database
            new_product = Products(**product_data)
            result = new_product.save()
            return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/order', methods=['GET', 'POST'])
def place_order():
    try:
        # Validate API key
        api_key = request.args.get('api_key')
        if not validate_api_key(api_key=api_key):
            return jsonify({"error": "Enter valid api key"})

        if request.method == 'POST':
            total_price = 0
            response = request.json
            orders = Orders(**response)

            # Calculate total price and update product stock
            for products in orders.product:
                product_info = mongo.db.products.find_one(
                    {'product_name': products['product_name']}) or {}
                if not product_info:
                    return jsonify({'error': 'Product not found'}), 404
                price_per_unit = product_info.get('price', 0)
                quantity = products.get('quantity', 0)
                total_price += quantity * price_per_unit

                # Update product stock
                mongo.db.products.update_one({'_id': product_info['_id']}, {
                    '$inc': {'stock': -products.get('quantity', 0)}})

            # Save order with total price
            orders.total_price = total_price
            orders.save()
            return jsonify({'data': 'Order placed successfully.'}), 201

        else:
            return jsonify({'error': 'Oops something went wrong'}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
