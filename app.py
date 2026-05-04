import streamlit as st
import pandas as pd

from scraper import Scraper
from report import PriceReport


st.set_page_config(
    page_title="Price Hunter",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Price Hunter")
st.write("Aplicație Python care extrage cărți și prețuri folosind requests și BeautifulSoup.")

st.info("Datele sunt extrase live de pe site-ul books.toscrape.com.")

st.sidebar.header("Filtre")

pages = st.sidebar.slider(
    "Câte pagini vrei să extragi?",
    min_value=1,
    max_value=5,
    value=1
)

search_text = st.sidebar.text_input(
    "Caută carte",
    placeholder="Ex: travel, music, mystery"
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
    with st.spinner("Se extrag datele..."):
        scraper = Scraper()
        products = scraper.get_products(pages=pages)

    st.session_state["products"] = products
    st.success(f"Au fost extrase {len(products)} cărți.")

if "products" in st.session_state:
    products = st.session_state["products"]
    report = PriceReport(products)

    filtered_products = report.filter_products(
        search_text=search_text,
        min_price=min_price,
        max_price=max_price,
        rating=rating
    )

    st.subheader("Cărți găsite")

    if filtered_products:
        df = pd.DataFrame([product.to_dict() for product in filtered_products])
        st.dataframe(df, use_container_width=True)

        cheapest = report.cheapest_product(filtered_products)
        expensive = report.most_expensive_product(filtered_products)
        average = report.average_price(filtered_products)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Număr cărți", len(filtered_products))
        col2.metric("Cel mai ieftin", f"{cheapest.price:.2f} £")
        col3.metric("Cel mai scump", f"{expensive.price:.2f} £")
        col4.metric("Preț mediu", f"{average:.2f} £")

        st.subheader("Cea mai ieftină carte")
        st.write(f"**{cheapest.name}**")
        st.write(f"Preț: {cheapest.price:.2f} £")
        st.write(f"Rating: {cheapest.rating}")
        st.write(cheapest.link)

    else:
        st.warning("Nu există cărți care respectă filtrele alese.")
else:
    st.info("Apasă pe butonul «Extrage cărți» pentru a începe.")