class Product:
    def __init__(self, name, store, price, color, category, link):
        self.name = name
        self.store = store
        self.price = float(price)
        self.color = color
        self.category = category
        self.link = link

    def to_dict(self):
        return {
            "Nume": self.name,
            "Magazin": self.store,
            "Pret": self.price,
            "Culoare": self.color,
            "Categorie": self.category,
            "Link": self.link
        }