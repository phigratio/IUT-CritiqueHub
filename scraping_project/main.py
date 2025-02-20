# main.py
from sumash_tech import get_all_categories, scrape_category_products
from apple_gadgets import get_all_categories as get_apple_categories, scrape_category_products as scrape_apple_products
from database import setup_database, save_to_database, check_database

def main():
    setup_database()  # MongoDB setup

    websites = [
        # {"name": "Sumash Tech", "url": "http://www.sumashtech.com", "scraper": get_all_categories, "scraper_products": scrape_category_products},
        {"name": "Apple Gadgets BD", "url": "https://www.applegadgetsbd.com/", "scraper": get_apple_categories, "scraper_products": scrape_apple_products}
    ]

    for site in websites:
        base_url = site["url"]
        category_urls = site["scraper"](base_url)

        for category_url in category_urls:
            category_name = category_url.split("/")[-1]  # Extract category name from URL
            category_products = site["scraper_products"](category_url)
            print(f"Scraped {len(category_products)} products from {category_url}")

            if category_products:
                save_to_database(site["name"], category_name, category_products)

    print("\n✅ Scraping complete. Data saved to MongoDB.\n")
    check_database()

if __name__ == "__main__":
    main()
