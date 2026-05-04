class PriceReport:
    def __init__(self, products):
        self.products = products

    def cheapest_product(self):
        if not self.products:
            return None
        return min(self.products, key=lambda product: product.price)

    def most_expensive_product(self):
        if not self.products:
            return None
        return max(self.products, key=lambda product: product.price)

    def average_price(self):
        if not self.products:
            return 0
        total = sum(product.price for product in self.products)
        return round(total / len(self.products), 2)