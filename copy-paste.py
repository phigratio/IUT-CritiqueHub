from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["scraped_data"]  # Database name

# Collection names
sumash_collection = db["products"]
apple_collection = db["apple_products"]  # Assuming you want to insert into this collection

def copy_and_update_products():
    # Fetch all products from Sumash Tech
    sumash_products = sumash_collection.find({"website": "Sumash Tech"})
    
    # Prepare and insert into Apple Gadgets BD
    for product in sumash_products:
        # Get the current price and increase by 1000
        current_price = product["price"]
        
        # Assuming price is a string like '৳ 50000', strip the currency and convert to int
        price_value = int(current_price.strip("৳ ").replace(",", ""))  # Clean price and convert to int
        updated_price = price_value + 1000  # Add 1000 to the current price
        
        # Create a product for Apple Gadgets BD with the updated price
        apple_product = {
            "website": "Apple Gadgets BD",
            "category": product["category"],  # Keep same category as Sumash Tech
            "name": product["name"],
            "price": f"৳ {updated_price:,}",  # Format price with comma separator
        }
        
        # Insert the new product into the Apple Gadgets BD collection
        try:
            apple_collection.insert_one(apple_product)
            print(f"✅ Stored: {apple_product['name']} | Price: {apple_product['price']}")
        except Exception as e:
            print(f"[ERROR] Failed to store {product['name']}: {e}")

# Run the function to copy products and update prices
copy_and_update_products()
