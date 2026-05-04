import streamlit as st
from scraper import Scraper
from report import PriceReport
from storage import Storage

st.set_page_config(page_title="Price Hunter", page_icon="📚", layout="wide")

st.title("📚 Price Hunter")


#st.write("Aplicație Python care extrage cărți și prețuri folosind requests și BeautifulSoup.")
#st.info("Datele sunt extrase live de pe site-ul books.toscrape.com.")
scraper = Scraper()

st.sidebar.title("Filtre")

category = st.sidebar.selectbox(
    "Alege genul",
    ["Toate"] + list(scraper.categories.keys())
)

min_price = st.sidebar.number_input(
    "Preț minim (£)",
    min_value=0.0,
    value=0.0
)

max_price = st.sidebar.number_input(
    "Preț maxim (£)",
    min_value=0.0,
    value=60.0
)

rating = st.sidebar.selectbox(
    "Rating",
    ["Toate", "One", "Two", "Three", "Four", "Five"]
)

if st.button("Extrage cărți"):
    with st.spinner("Se extrag datele de pe toate paginile..."):
        products = scraper.get_products(category)

    st.success(f"Au fost extrase {len(products)} cărți.")

    filtered_products = []

    for product in products:
        if product.price < min_price:
            continue

        if product.price > max_price:
            continue

        if rating != "Toate" and product.rating != rating:
            continue

        filtered_products.append(product)

    st.subheader("Cărți găsite")

    if filtered_products:
        report = PriceReport(filtered_products)
        storage = Storage()
        storage.save_to_csv(filtered_products)

        col1, col2, col3 = st.columns(3)

        cheapest = report.cheapest_product()
        expensive = report.most_expensive_product()

        col1.metric("Număr cărți", len(filtered_products))
        col2.metric("Cel mai mic preț", f"£{cheapest.price}")
        col3.metric("Preț mediu", f"£{report.average_price()}")

        st.table([product.to_dict() for product in filtered_products])
        #st.success("Datele filtrate au fost salvate în products.csv.")
    else:
        st.warning("Nu există cărți care respectă filtrele alese.")
else:
    st.info("Apasă pe butonul de mai sus ca să extragi cărțile.")