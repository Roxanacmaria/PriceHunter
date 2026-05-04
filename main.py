from scraper import Scraper
from report import PriceReport


def main():
    scraper = Scraper()

    products = scraper.get_products(
        search_text="dress",
        category="rochii"
    )

    if not products:
        print("Nu au fost gasite produse.")
        return

    report = PriceReport(products)

    filtered_products = report.filter_products(
        min_price=0,
        max_price=100,
        color="Toate"
    )

    print("Produse extrase de pe ASOS:")

    for product in filtered_products:
        print(
            f"{product.name} | {product.price} £ | "
            f"{product.color} | {product.link}"
        )

    cheapest = report.cheapest_product(filtered_products)
    average = report.average_price(filtered_products)

    print("\nRaport:")
    print(f"Numar produse: {len(filtered_products)}")

    if cheapest:
        print(f"Cel mai ieftin produs: {cheapest.name} - {cheapest.price} £")

    print(f"Pret mediu: {average:.2f} £")


if __name__ == "__main__":
    main()