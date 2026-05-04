import re
import requests
from bs4 import BeautifulSoup
from product import Product


class Scraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def clean_price(self, price_text):
        price_text = price_text.replace(",", ".")
        price_text = re.sub(r"[^\d.]", "", price_text)

        if price_text == "":
            return None

        try:
            return float(price_text)
        except ValueError:
            return None

    def get_products(self):
        products = []

        products.extend(self.scrape_hm())
        products.extend(self.scrape_zara())

        return products

    def scrape_hm(self):
        url = "https://www2.hm.com/en_gb/ladies/shop-by-product/tops.html"
        products = []

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            return products

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select("article, li")

        for item in items:
            text = item.get_text(" ", strip=True)

            if "£" not in text:
                continue

            name_tag = item.find(["h2", "h3", "a"])
            price_match = re.search(r"£\s*\d+(\.\d{1,2})?", text)

            if not name_tag or not price_match:
                continue

            name = name_tag.get_text(" ", strip=True)
            price = self.clean_price(price_match.group())

            if not name or price is None:
                continue

            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else url

            if link.startswith("/"):
                link = "https://www2.hm.com" + link

            color = self.detect_color(text)
            category = "topuri"

            product = Product(
                name=name,
                store="H&M",
                price=price,
                color=color,
                category=category,
                link=link
            )

            products.append(product)

            if len(products) >= 30:
                break

        return products

    def scrape_zara(self):
        url = "https://www.zara.com/uk/en/woman-tshirts-l1362.html"
        products = []

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            return products

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select("article, li, div")

        for item in items:
            text = item.get_text(" ", strip=True)

            if "£" not in text:
                continue

            price_match = re.search(r"£\s*\d+(\.\d{1,2})?", text)

            if not price_match:
                continue

            price = self.clean_price(price_match.group())

            if price is None:
                continue

            name_tag = item.find(["h2", "h3", "a"])
            name = name_tag.get_text(" ", strip=True) if name_tag else "Produs Zara"

            if len(name) < 3:
                name = "Produs Zara"

            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else url

            if link.startswith("/"):
                link = "https://www.zara.com" + link

            color = self.detect_color(text)

            product = Product(
                name=name,
                store="Zara",
                price=price,
                color=color,
                category="tricouri",
                link=link
            )

            products.append(product)

            if len(products) >= 30:
                break

        return products

    def detect_color(self, text):
        colors = {
            "black": "negru",
            "white": "alb",
            "red": "rosu",
            "blue": "albastru",
            "green": "verde",
            "pink": "roz",
            "beige": "bej",
            "grey": "gri",
            "gray": "gri",
            "brown": "maro",
            "yellow": "galben"
        }

        text = text.lower()

        for english_color, romanian_color in colors.items():
            if english_color in text:
                return romanian_color

        return "necunoscut"