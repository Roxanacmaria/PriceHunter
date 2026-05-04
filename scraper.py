import re
import requests
from bs4 import BeautifulSoup
from product import Product


class Scraper:
    def __init__(self):
        self.base_url = "http://books.toscrape.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def clean_price(self, price_text):
        price_text = re.sub(r"[^\d.]", "", price_text)
        return float(price_text)

    def get_products(self, pages=1):
        products = []

        for page in range(1, pages + 1):
            if page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}catalogue/page-{page}.html"

            response = requests.get(url, headers=self.headers)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".product_pod")

            for item in items:
                name = item.h3.a["title"]
                price_text = item.select_one(".price_color").text
                price = self.clean_price(price_text)

                availability = item.select_one(".availability").text.strip()

                rating_classes = item.select_one(".star-rating")["class"]
                rating = rating_classes[1]

                link = item.h3.a["href"]

                if not link.startswith("catalogue"):
                    link = "catalogue/" + link

                full_link = self.base_url + link

                product = Product(
                    name=name,
                    price=price,
                    availability=availability,
                    rating=rating,
                    category="Books",
                    link=full_link
                )

                products.append(product)

        return products