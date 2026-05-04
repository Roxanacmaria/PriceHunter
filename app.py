import streamlit as st
import pandas as pd

from scraper import Scraper
from report import PriceReport


st.set_page_config(
    page_title="Price Hunter ASOS",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Price Hunter - ASOS")
st.write("Aplicație Python care extrage produse live de pe ASOS folosind requests și BeautifulSoup.")

st.sidebar.header("Căutare produse")

search_query = st.sidebar.text_input(
    "Ce produs cauți?",
    value="dress",
    placeholder="Ex: dress, shirt, jeans, shoes"
)

category = st.sidebar.selectbox(
    "Categorie",
    ["haine", "rochii", "tricouri", "jeans", "pantofi", "accesorii"]
)

min_price = st.sidebar.number_input(
    "Preț minim (£)",
    min_value=0.0,
    value=0.0
)

max_price = st.sidebar.number_input(
    "Preț maxim (£)",
    min_value=0.0,
    value=100.0
)

if st.button("Extrage produse de pe ASOS"):
    with st.spinner("Se extrag produsele de pe ASOS..."):
        scraper = Scraper()
        products = scraper.get_products(
            search_text=search_query,
            category=category
        )

    if not products:
        st.error(
            "Nu au fost găsite produse. ASOS poate încărca produsele prin JavaScript "
            "sau poate bloca temporar cererile automate."
        )
    else:
        st.session_state["products"] = products
        st.success(f"Au fost extrase {len(products)} produse.")

if "products" in st.session_state:
    products = st.session_state["products"]

    colors = ["Toate"] + sorted(set(product.color for product in products))

    color = st.sidebar.selectbox(
        "Culoare",
        colors
    )

    report = PriceReport(products)

    filtered_products = report.filter_products(
        search_text="",
        min_price=min_price,
        max_price=max_price,
        color=color
    )

    st.subheader("Produse găsite")

    if filtered_products:
        df = pd.DataFrame([product.to_dict() for product in filtered_products])
        st.dataframe(df, use_container_width=True)

        cheapest = report.cheapest_product(filtered_products)
        average = report.average_price(filtered_products)

        col1, col2, col3 = st.columns(3)

        col1.metric("Număr produse", len(filtered_products))
        col2.metric("Cel mai ieftin", f"{cheapest.price:.2f} £")
        col3.metric("Preț mediu", f"{average:.2f} £")

        st.subheader("Cel mai ieftin produs")
        st.write(f"**{cheapest.name}**")
        st.write(f"Preț: {cheapest.price:.2f} £")
        st.write(f"Culoare detectată: {cheapest.color}")
        st.write(cheapest.link)
    else:
        st.warning("Nu există produse care respectă filtrele alese.")
else:
    st.info("Alege un produs din sidebar și apasă pe butonul de extragere.")