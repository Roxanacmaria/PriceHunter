import re
import requests
from bs4 import BeautifulSoup
from product import Product


class Scraper:
    def __init__(self):
        self.store = "ASOS"
        self.base_url = "https://www.asos.com"
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
            "yellow": "galben",
            "orange": "portocaliu",
            "purple": "mov",
            "cream": "crem",
            "navy": "bleumarin"
        }

        text = text.lower()

        for english_color, romanian_color in colors.items():
            if english_color in text:
                return romanian_color

        return "necunoscut"

    def build_search_url(self, search_text):
        search_text = search_text.strip().replace(" ", "+")
        return f"https://www.asos.com/search/?q={search_text}"

    def get_products(self, search_text="dress", category="haine"):
        url = self.build_search_url(search_text)
        return self.scrape_asos(url, category)

    def scrape_asos(self, url, category):
        products = []

        response = requests.get(url, headers=self.headers, timeout=15)

        if response.status_code != 200:
            return products

        soup = BeautifulSoup(response.text, "html.parser")

        product_cards = soup.select("article")

        if not product_cards:
            product_cards = soup.select("li")

        for card in product_cards:
            text = card.get_text(" ", strip=True)

            if "£" not in text:
                continue

            price_match = re.search(r"£\s*\d+(\.\d{1,2})?", text)

            if not price_match:
                continue

            price = self.clean_price(price_match.group())

            if price is None:
                continue

            name_tag = card.find(["h2", "h3", "a"])
            name = name_tag.get_text(" ", strip=True) if name_tag else "Produs ASOS"

            if len(name) < 3:
                name = "Produs ASOS"

            link_tag = card.find("a", href=True)
            link = link_tag["href"] if link_tag else url

            if link.startswith("/"):
                link = self.base_url + link

            color = self.detect_color(text)

            product = Product(
                name=name,
                store=self.store,
                price=price,
                color=color,
                category=category,
                link=link
            )

            products.append(product)

            if len(products) >= 40:
                break

        return products