import json 
import os
from sqlalchemy import create_engine , Column , Integer , String,ForeignKey
from sqlalchemy . ext . declarative import declarative_base
from sqlalchemy . orm import sessionmaker , relationship

current_directory = os . path . dirname ( os . path . abspath ( __file__ ) )
database_path = os . path . join ( current_directory , 'books. db ')
engine = create_engine (f"sqlite :///{ database_path }")
data={
    "store": {
        "name": "Tech Hub",
        "location": {
            "city": "San Francisco",
            "address": {
                "street": "123 Market St",
                "postalCode": "94103"
            }
        },
        "departments": [
            {
                "name": "Electronics",
                "products": [
                    {
                        "id": 201,
                        "name": "Laptop",
                        "brand": "BrandX",
                        "price": 999.99,
                        "specifications": {
                            "processor": "Intel i7",
                            "memory": "16GB",
                            "storage": "512GB SSD"
                        }
                    },
                    {
                        "id": 202,
                        "name": "Smartphone",
                        "brand": "BrandY",
                        "price": 799.99,
                        "specifications": {
                            "screenSize": "6.1 inches",
                            "battery": "4000mAh",
                            "camera": "12MP"
                        }
                    }
                ]
            },
            {
                "name": "Accessories",
                "products": [
                    {
                        "id": 301,
                        "name": "Wireless Mouse",
                        "brand": "BrandZ",
                        "price": 29.99,
                        "specifications": {
                            "batteryLife": "12 months",
                            "connectivity": "Bluetooth"
                        }
                    },
                    {
                        "id": 302,
                        "name": "Keyboard",
                        "brand": "BrandX",
                        "price": 49.99,
                        "specifications": {
                            "layout": "QWERTY",
                            "connectivity": "Wireless"
                        }
                    }
                ]
            }
        ]
    }
}

print("Store Name: ",data["store"]["name"])
print("City Location: ",data["store"]["location"]["city"]);

for department in data["store"]["departments"]:
  if department["name"]=="Electronics":
    for product in department["products"]:
      print("Product Name: ",product["name"])
      print("Price: ",product["price"]);
      
for department in data["store"]["departments"]:
  for product in department["products"]:
    if product["name"]=="Wireless Mouse":
      print("Brand: ",product["brand"])
      print("Specifications: ",product["specifications"])
      
      
for department in data["store"]["departments"]:
    for product in department["products"]:
        if product["name"] == "Smartphone":
            product["price"] = 749.99

print("Updated JSON:")
print(json.dumps(data))


Base=declarative_base()

class Book(Base):
  __tablename__='books'
  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  author = Column(String, nullable=False)
  published_year = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)
  
  
engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)



new_book = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", published_year=1925, price=10.99)
session.add(new_book)
session.commit()

books = session.query(Book).all()
for book in books:
    print(f"Title: {book.title}, Author: {book.author}, Published Year: {book.published_year}, Price: {book.price}")
    
book_to_update = session.query(Book).filter_by(title="The Great Gatsby").first()
if book_to_update:
    book_to_update.price = 12.99
    session.commit()
