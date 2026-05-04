class Product:
    def __init__(self, name, price, availability, rating, category, link):
        self.name = name
        self.price = float(price)
        self.availability = availability
        self.rating = rating
        self.category = category
        self.link = link

    def to_dict(self):
        return {
            "Titlu": self.name,
            "Pret": self.price,
            "Disponibilitate": self.availability,
            "Rating": self.rating,
            "Categorie": self.category,
            "Link": self.link
        }