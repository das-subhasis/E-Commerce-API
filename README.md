# E-Commerce-API

Welcome to **Your Flask API Project Name**! This project serves as an example Flask API implementation. It includes user registration, product management, and order placement functionalities.

## Features

- User registration: Allows users to register with their email and other details.
- User retrieval: Retrieves all users or a specific user by ID.
- Product management: Retrieves all products or adds a new product.
- Order placement: Places an order for products, updating the product stock accordingly.

## Installation

1. Clone the repository:

```cmd
git clone https://github.com/yourusername/your-flask-api-project.git
```

2. Navigate to the project directory:
```
cd E-Commerce-API   
```

3. Install the depemdencies:
```
pip install -r requirements.txt
```

4. Initiate the server
```
python run.py
```

## API Documentation
- /register: [POST] Register a new user.
  ```
   user_data = {
    "username": 'davyjones',
    "email": 'potc@gmail.com',
    "firstName": 'Davy',
    "lastName": 'Jones',
    "password": 'jacksparrow'
  }
  ```
- /users: [GET] Get all users.
- /users/<user_id>: [GET] Get user by ID.
- /products: [GET, POST] Get all products or add a new product.
  ```
   product_data = {
    product_name = 'iphone-12',
    description: 'a very expensive phone with minimal advantages',
    price: 100000,
    stock: 21
  }
  ```
- /order: [POST] Place an order.
  ```
    order_data = {
    "user_id": "1",
    "product": [
        {
            "product_name": "iphone-12",
            "quantity": 2
        },
        {
            "product_name": "samsung-galaxy-s11",
            "quantity": 1
        }
    ]
  }  
  ```

