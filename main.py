from scraper import Scraper
from report import PriceReport


def main():
    scraper = Scraper()
    products = scraper.get_products(pages=1)

    report = PriceReport(products)

    filtered_products = report.filter_products(
        search_text="",
        min_price=0,
        max_price=60,
        rating="Toate"
    )

    print("Carti extrase:")

    for product in filtered_products:
        print(
            f"{product.name} | {product.price} £ | "
            f"{product.rating} | {product.availability}"
        )

    cheapest = report.cheapest_product(filtered_products)
    expensive = report.most_expensive_product(filtered_products)
    average = report.average_price(filtered_products)

    print("\nRaport:")
    print(f"Numar carti: {len(filtered_products)}")
    print(f"Cea mai ieftina carte: {cheapest.name} - {cheapest.price} £")
    print(f"Cea mai scumpa carte: {expensive.name} - {expensive.price} £")
    print(f"Pret mediu: {average:.2f} £")


if __name__ == "__main__":
    main()