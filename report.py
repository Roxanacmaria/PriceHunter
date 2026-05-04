class PriceReport:
    def __init__(self, products):
        self.products = products

    def filter_products(
        self,
        search_text="",
        min_price=0,
        max_price=9999,
        rating="Toate"
    ):
        filtered = []

        for product in self.products:
            search_ok = search_text.lower() in product.name.lower()
            price_ok = min_price <= product.price <= max_price
            rating_ok = rating == "Toate" or product.rating == rating

            if search_ok and price_ok and rating_ok:
                filtered.append(product)

        return filtered

    def cheapest_product(self, products):
        if not products:
            return None

        return min(products, key=lambda product: product.price)

    def most_expensive_product(self, products):
        if not products:
            return None

        return max(products, key=lambda product: product.price)

    def average_price(self, products):
        if not products:
            return 0

        total = sum(product.price for product in products)
        return total / len(products)