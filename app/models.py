from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
import bcrypt
from .extensions import mongo

# create salt for encrypting password
salt = bcrypt.gensalt(12)

# Database models fot our APU

# Add your custom model here

class User(BaseModel):
    # Validating data type for each attribute
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    password: str
    createdAt: datetime.datetime = datetime.datetime.now()

    # custom method to insert data 
    def save(self):
        try:
            user_data = {
                "username": self.username,
                "email": self.email,
                "firstName": self.firstName,
                "lastName": self.lastName,
                "password": bcrypt.hashpw(self.password.encode('utf-8'), salt=salt), # hash password before saving
                "createdAt": self.createdAt
            }

            mongo.db.users.insert_one(user_data)
        except Exception as error:
            return {"Operation": "Failure", "error": str(error)}
        return {"Operation": "Successful"}


class Products(BaseModel):
    # Validating data type for each attribute
    product_name: str
    description: str
    price: float
    stock: int
    createdAt: datetime.datetime = datetime.datetime.now()

    def save(self):
        try:
            product_data = {
                "product_name": self.product_name.replace(' ', '-'),
                "product_type": self.product_type,
                "description": self.description,
                "price": self.price,
                "stock": self.quantity,
                "createdAt": self.createdAt
            }

            mongo.db.products.insert_one(product_data)
        except Exception as error:
            return {"data": "Failure", "error": str(error)}
        return {"data": "data inserted successfully"}


class Orders(BaseModel):
    # Validating data type for each attribute
    user_id: str
    product: list[dict]
    total_price: float = 0.0
    createdAt: datetime.datetime = datetime.datetime.now()

    def save(self):
        try:
            order_data = {
                "user_id": self.user_id,
                "product": self.product,
                "total_price": self.total_price,
                "createdAt": self.createdAt,
            }

            mongo.db.orders.insert_one(order_data)
        except Exception as error:
            return {"Operation": "Failure", "error": str(error)}
        return {"data": "data inserted successfully"}
