import requests
from bs4 import BeautifulSoup
import re
from product import Product


class Scraper:
    def __init__(self):
        self.base_url = "http://books.toscrape.com/"
        self.categories = {
            "Travel": "catalogue/category/books/travel_2/index.html",
            "Mystery": "catalogue/category/books/mystery_3/index.html",
            "Historical Fiction": "catalogue/category/books/historical-fiction_4/index.html",
            "Sequential Art": "catalogue/category/books/sequential-art_5/index.html",
            "Classics": "catalogue/category/books/classics_6/index.html",
            "Philosophy": "catalogue/category/books/philosophy_7/index.html",
            "Romance": "catalogue/category/books/romance_8/index.html",
            "Womens Fiction": "catalogue/category/books/womens-fiction_9/index.html",
            "Fiction": "catalogue/category/books/fiction_10/index.html",
            "Childrens": "catalogue/category/books/childrens_11/index.html",
            "Religion": "catalogue/category/books/religion_12/index.html",
            "Nonfiction": "catalogue/category/books/nonfiction_13/index.html",
            "Music": "catalogue/category/books/music_14/index.html",
            "Default": "catalogue/category/books/default_15/index.html",
            "Science Fiction": "catalogue/category/books/science-fiction_16/index.html",
            "Sports and Games": "catalogue/category/books/sports-and-games_17/index.html",
            "Add a comment": "catalogue/category/books/add-a-comment_18/index.html",
            "Fantasy": "catalogue/category/books/fantasy_19/index.html",
            "New Adult": "catalogue/category/books/new-adult_20/index.html",
            "Young Adult": "catalogue/category/books/young-adult_21/index.html",
            "Science": "catalogue/category/books/science_22/index.html",
            "Poetry": "catalogue/category/books/poetry_23/index.html",
            "Paranormal": "catalogue/category/books/paranormal_24/index.html",
            "Art": "catalogue/category/books/art_25/index.html",
            "Psychology": "catalogue/category/books/psychology_26/index.html",
            "Autobiography": "catalogue/category/books/autobiography_27/index.html",
            "Parenting": "catalogue/category/books/parenting_28/index.html",
            "Adult Fiction": "catalogue/category/books/adult-fiction_29/index.html",
            "Humor": "catalogue/category/books/humor_30/index.html",
            "Horror": "catalogue/category/books/horror_31/index.html",
            "History": "catalogue/category/books/history_32/index.html",
            "Food and Drink": "catalogue/category/books/food-and-drink_33/index.html",
            "Christian Fiction": "catalogue/category/books/christian-fiction_34/index.html",
            "Business": "catalogue/category/books/business_35/index.html",
            "Biography": "catalogue/category/books/biography_36/index.html",
            "Thriller": "catalogue/category/books/thriller_37/index.html",
            "Contemporary": "catalogue/category/books/contemporary_38/index.html",
            "Spirituality": "catalogue/category/books/spirituality_39/index.html",
            "Academic": "catalogue/category/books/academic_40/index.html",
            "Self Help": "catalogue/category/books/self-help_41/index.html",
            "Historical": "catalogue/category/books/historical_42/index.html",
            "Christian": "catalogue/category/books/christian_43/index.html",
            "Suspense": "catalogue/category/books/suspense_44/index.html",
            "Short Stories": "catalogue/category/books/short-stories_45/index.html",
            "Novels": "catalogue/category/books/novels_46/index.html",
            "Health": "catalogue/category/books/health_47/index.html",
            "Politics": "catalogue/category/books/politics_48/index.html",
            "Cultural": "catalogue/category/books/cultural_49/index.html",
            "Erotica": "catalogue/category/books/erotica_50/index.html",
            "Crime": "catalogue/category/books/crime_51/index.html",
        }

    def get_products(self, selected_category="Toate"):
        products = []

        if selected_category == "Toate":
            categories_to_scrape = self.categories.items()
        else:
            categories_to_scrape = [(selected_category, self.categories[selected_category])]

        for category_name, category_url in categories_to_scrape:
            products.extend(self._scrape_category(category_name, category_url))

        return products

    def _scrape_category(self, category_name, category_url):
        products = []
        page = 1

        while True:
            if page == 1:
                url = self.base_url + category_url
            else:
                url = self.base_url + category_url.replace(
                    "index.html",
                    f"page-{page}.html"
                )

            response = requests.get(url)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".product_pod")

            if not items:
                break

            for item in items:
                name = item.h3.a["title"]

                price_text = item.select_one(".price_color").text
                price_text = re.sub(r"[^\d.]", "", price_text)
                price = float(price_text)

                rating_class = item.select_one("p.star-rating")["class"]
                rating = rating_class[1]

                products.append(Product(name, price, rating, category_name))

            page += 1

        return products