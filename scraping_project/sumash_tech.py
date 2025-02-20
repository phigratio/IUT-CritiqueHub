# sumash_tech.py
from base_scraper import fetch_page, random_sleep

# Scrape all categories from Sumash Tech
def get_all_categories(base_url):
    soup = fetch_page(base_url)
    if not soup:
        return []

    category_links = []
    category_elements = soup.select("div.cat-items-list a")

    for element in category_elements:
        href = element.get("href")
        if href.startswith("http"):
            category_links.append(href)
        else:
            category_links.append(base_url.rstrip("/") + "/" + href.lstrip("/"))

    print(f"[INFO] Found {len(category_links)} categories on {base_url}")
    return category_links

# Scrape products from a Sumash Tech category
def scrape_category_products(category_url):
    page = 1
    category_products = []

    while True:
        url = f"{category_url}?page={page}"
        soup = fetch_page(url)
        if not soup:
            break

        product_elements = soup.find_all("div", class_="product__items")
        if not product_elements:
            break

        for product in product_elements:
            pro_name = product.find("h3", class_="product__title")
            price_span = product.find("div", class_="product__price").find("strong")

            if not pro_name or not price_span:
                print(f"[WARNING] Missing data on {url}")
                continue

            pro_name = pro_name.get_text(strip=True)

            del_tag = price_span.find("del")
            if del_tag:
                del_tag.decompose()

            current_price = price_span.get_text(strip=True)

            category_products.append({
                "name": pro_name,
                "current_price": current_price,
            })

        page += 1
        random_sleep()

    return category_products
