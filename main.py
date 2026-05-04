from scraper import Scraper
from report import PriceReport
from storage import Storage


def main():
    scraper = Scraper()
    products = scraper.get_products("Toate")

    report = PriceReport(products)
    storage = Storage()

    storage.save_to_csv(products)

    print(f"Au fost extrase {len(products)} cărți.")

    cheapest = report.cheapest_product()
    expensive = report.most_expensive_product()

    if cheapest:
        print(f"Cea mai ieftină carte: {cheapest.name} - £{cheapest.price}")

    if expensive:
        print(f"Cea mai scumpă carte: {expensive.name} - £{expensive.price}")

    print(f"Preț mediu: £{report.average_price()}")


if __name__ == "__main__":
    main()