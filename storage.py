import csv


class Storage:
    def __init__(self, filename="products.csv"):
        self.filename = filename

    def save_to_csv(self, products):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["Titlu", "Pret", "Rating", "Categorie"])

            for product in products:
                writer.writerow([
                    product.name,
                    product.price,
                    product.rating,
                    product.category
                ])