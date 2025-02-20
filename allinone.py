import requests
from bs4 import BeautifulSoup
import random
import time
import sqlite3

# User-Agent to prevent blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# List of proxies (You can add more if needed)
proxies_list = [
    {"http": "http://220.248.70.237:9002"},
    {"http": "http://123.30.154.171:7777"}
]

# Select a random proxy
def get_random_proxy():
    return random.choice(proxies_list)

# ✅ STEP 1: SETUP DATABASE
def setup_database():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            category TEXT,
            name TEXT,
            price TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[INFO] Database setup complete.")

# ✅ STEP 2: SAVE DATA TO DATABASE
def save_to_database(website, category, products):
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()

    if len(products) == 0:
        print(f"[WARNING] No products to save for {website} - {category}")
        return

    print(f"\n[INFO] Saving {len(products)} products from {website} - {category} to the database...\n")

    for product in products:
        print(f"Storing: {product['name']} | Price: {product['current_price']}")
        cursor.execute("INSERT INTO products (website, category, name, price) VALUES (?, ?, ?, ?)", 
                       (website, category, product["name"], product["current_price"]))

    conn.commit()
    conn.close()

# ✅ STEP 3: SCRAPE ALL CATEGORIES FROM A WEBSITE
def get_all_categories(base_url):
    try:
        proxy = get_random_proxy()
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup.prettify())  # This will print the HTML of the page for inspection

        category_links = []

        # Extract category links (Modify selector if needed)
        category_elements = soup.select("div.cat-items-list a")

        for element in category_elements:
            href = element.get("href")
            if href.startswith("http"):
                category_links.append(href)
            else:
                category_links.append(base_url.rstrip("/") + "/" + href.lstrip("/"))

        print(f"\n[DEBUG] Found {len(category_links)} categories on {base_url}")
        return category_links
    except requests.RequestException as e:
        print("[ERROR] Error fetching categories:", e)
        return []

# ✅ STEP 4: SCRAPE PRODUCTS FROM A CATEGORY
def scrape_category_products(category_url):
    page = 1
    category_products = []

    while True:
        try:
            proxy = get_random_proxy()
            url = f"{category_url}?page={page}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            product_elements = soup.find_all("div", class_="product__items")

            if not product_elements:
                break  # No more products

            for product in product_elements:
                pro_name = product.find("h3", class_="product__title")
                price_span = product.find("div", class_="product__price").find("strong")

                if not pro_name or not price_span:
                    print(f"[WARNING] Missing data on {url}")
                    continue

                pro_name = pro_name.get_text(strip=True)

                # Check for discounted price (if exists)
                del_tag = price_span.find("del")
                if del_tag:
                    del_tag.decompose()

                current_price = price_span.get_text(strip=True)


                category_products.append({
                    "name": pro_name,
                    "current_price": current_price,
                })

            if len(category_products) == 0:
                print("[WARNING] No products scraped from", url)

            page += 1
            time.sleep(random.uniform(1, 3))

        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch products from {category_url}: {e}")
            break

    return category_products


# ✅ STEP 5: VERIFY IF DATA IS STORED IN DATABASE
def check_database():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    print(f"\n[INFO] Total products stored in database: {total_products}")

    cursor.execute("SELECT * FROM products LIMIT 10")
    rows = cursor.fetchall()

    if not rows:
        print("[WARNING] No data found in database!")
    else:
        print("\n[INFO] Sample Data from Database:")
        for row in rows:
            print(row)

    conn.close()

# ✅ STEP 6: MAIN SCRIPT TO RUN SCRAPER
def main():
    setup_database()

    websites = [
        {"name": "Sumash Tech", "url": "http://www.sumashtech.com"},
        {"name": "Apple Gadgets BD", "url": "https://www.applegadgetsbd.com/"}
    ]

    for site in websites:
        base_url = site["url"]
        category_urls = get_all_categories(base_url)

        for category_url in category_urls:
            category_name = category_url.split("/")[-1]  # Extract category name from URL
            category_products = scrape_category_products(category_url)
            print(f"Scraped {len(category_products)} products from {category_url}")

            if category_products:
                save_to_database(site["name"], category_name, category_products)

    print("\n✅ Scraping complete. Data saved to database.\n")
    check_database()

# Run the script
if __name__ == "__main__":
    main()
