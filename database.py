# database.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change this if using a remote MongoDB
db = client["scraped_data"]  # Database name
collection = db["products"]  # Collection name

def setup_database():
    """Ensure indexes for fast queries."""
    collection.create_index([("name", 1)], unique=True)
    print("[INFO] Connected to MongoDB. Database and collection set up.")

def save_to_database(website, category, products):
    """Save product data to MongoDB."""
    if len(products) == 0:
        print(f"[WARNING] No products to save for {website} - {category}")
        return

    print(f"\n[INFO] Saving {len(products)} products from {website} - {category} to MongoDB...\n")

    for product in products:
        product_data = {
            "website": website,
            "category": category,
            "name": product["name"],
            "price": product["current_price"],
        }
        
        try:
            collection.insert_one(product_data)
            print(f"✅ Stored: {product['name']} | Price: {product['current_price']}")
        except Exception as e:
            print(f"[ERROR] Failed to store {product['name']}: {e}")

def check_database():
    """Check the number of records in MongoDB and display some sample data."""
    total_products = collection.count_documents({})
    print(f"\n[INFO] Total products stored in database: {total_products}")

    sample_products = collection.find().limit(10)
    print("\n[INFO] Sample Data from Database:")
    for product in sample_products:
        print(product)

