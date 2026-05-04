class Product:
    def __init__(self, name, price, rating, category):
        self.name = name
        self.price = price
        self.rating = rating
        self.category = category

    def to_dict(self):
        return {
            "Titlu": self.name,
            "Preț (£)": self.price,
            "Rating": self.rating,
            "Categorie": self.category
        }