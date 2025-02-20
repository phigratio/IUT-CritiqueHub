from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["scraped_data"]

@app.route('/compare-products')
def compare_products():
    return render_template('compare_products.html')

@app.route('/compare', methods=['GET'])
def compare():
    query = request.args.get('product')
    if query:
        sumash_product = db["products"].find_one({"name": {"$regex": query, "$options": "i"}, "website": "Sumash Tech"})
        apple_product = db["apple_products"].find_one({"name": {"$regex": query, "$options": "i"}, "website": "Apple Gadgets BD"})

        product_data = []
        if sumash_product and apple_product:
            product_data.append({
                "name": sumash_product["name"],
                "apple_gadgets_bd_price": apple_product["price"],
                "sumash_tech_price": sumash_product["price"]
            })

        return jsonify(product_data)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
