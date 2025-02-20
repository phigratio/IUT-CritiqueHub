# apple_gadgets.py
from base_scraper import fetch_page, random_sleep

# Scrape all categories from Apple Gadgets BD
def get_all_categories(base_url):
    soup = fetch_page(base_url)
    if not soup:
        return []

    category_links = []
    # Scrape all categories from Apple Gadgets BD
def get_all_categories(base_url):
    soup = fetch_page(base_url)
    if not soup:
        return []

    category_links = []
    category_elements = {
        "Phones & Tablets": {
            "url": "/category/phones-tablets",
            "subcategories": {
                "iPad & TAB": "https://www.applegadgetsbd.com/category/phones-tablets/ipad-and-tab",
                "iPhone": "https://www.applegadgetsbd.com/category/phones-tablets/iphone",
                "SAMSUNG": "https://www.applegadgetsbd.com/category/phones-tablets/samsung",
                "Google": "https://www.applegadgetsbd.com/category/phones-tablets/google",
                "Xiaomi": "https://www.applegadgetsbd.com/category/phones-tablets/xiaomi",
                "Amazon": "https://www.applegadgetsbd.com/category/phones-tablets/amazon",
                "OnePlus": "https://www.applegadgetsbd.com/category/phones-tablets/oneplus",
                "Nokia": "https://www.applegadgetsbd.com/category/phones-tablets/nokia",
                "realme": "https://www.applegadgetsbd.com/category/phones-tablets/realme",
                "NOTHING": "https://www.applegadgetsbd.com/category/phones-tablets/nothing",
                "HUAWEI": "https://www.applegadgetsbd.com/category/phones-tablets/huawei",
                "Infinix": "https://www.applegadgetsbd.com/category/phones-tablets/infinix",
                "OPPO": "https://www.applegadgetsbd.com/category/phones-tablets/oppo",
                "Tecno": "https://www.applegadgetsbd.com/category/phones-tablets/tecno",
                "vivo": "https://www.applegadgetsbd.com/category/phones-tablets/vivo",
                "Motorola": "https://www.applegadgetsbd.com/category/phones-tablets/motorola",
                "ASUS": "https://www.applegadgetsbd.com/category/phones-tablets/asus",
                "ZTE": "https://www.applegadgetsbd.com/category/phones-tablets/zte",
                "Balmuda": "https://www.applegadgetsbd.com/category/phones-tablets/balmuda",
            },
        },
    }

    # Loop through categories
    for category, data in category_elements.items():
        href = data["url"]
        if href.startswith("http"):
            category_links.append(href)
        else:
            category_links.append(base_url.rstrip("/") + "/" + href.lstrip("/"))
        
        # Add subcategories as well
        for subcategory_name, subcategory_url in data["subcategories"].items():
            category_links.append(subcategory_url)

    print(f"[INFO] Found {len(category_links)} categories on {base_url}")
    return category_links


    for element in category_elements:
        href = element.get("href")
        if href.startswith("http"):
            category_links.append(href)
        else:
            category_links.append(base_url.rstrip("/") + "/" + href.lstrip("/"))

    print(f"[INFO] Found {len(category_links)} categories on {base_url}")
    return category_links

# Scrape products from an Apple Gadgets BD category
def scrape_category_products(category_url):
    page = 1
    category_products = []

    while True:
        url = f"{category_url}?page={page}"
        soup = fetch_page(url)
        if not soup:
            break

        product_elements = soup.find_all("div", class_=r"grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-4 mt-8 print:mt-4 print:sm:grid-cols-5 print:gap-1")
        if not product_elements:
            break

        for product in product_elements:
            pro_name = product.find("p", class_="font-SFProDisplaySemibold.text-sm.mt-5.px-3")
            price_span = product.find("p", class_=r"font-SFProDisplaySemibold text-tiny my-2 group-hover:text-primary duration-300")

        if price_span:
            price = price_span.text.strip().split("৳")[1]  # Extract price without the symbol
        else:
            price = None


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


