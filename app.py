from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DATA_PATH = Path("data/vehicles_us.csv")


st.set_page_config(
    page_title="TripleTen EDA",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TripleTen EDA")
st.write("Analisis exploratorio de anuncios de coches usados.")

if DATA_PATH.exists():
    car_data = pd.read_csv(DATA_PATH)
    st.caption(f"Dataset cargado: {DATA_PATH}")
else:
    uploaded_file = st.file_uploader("Carga un archivo CSV", type=["csv"])

    if uploaded_file is None:
        st.info("Coloca el dataset en data/vehicles_us.csv o carga un CSV.")
        st.stop()

    car_data = pd.read_csv(uploaded_file)

st.header("Vista previa del conjunto de datos")
st.dataframe(car_data.head(), width="stretch")

st.header("Resumen estadistico")
st.dataframe(car_data.describe(include="all").astype(str), width="stretch")

st.header("Visualizaciones")

hist_button = st.button("Construir histograma")
scatter_button = st.button("Construir grafico de dispersion")

if hist_button:
    st.write(
        "Creacion de un histograma para el conjunto de datos de anuncios de "
        "venta de coches."
    )
    fig = go.Figure(data=[go.Histogram(x=car_data["odometer"])])
    fig.update_layout(
        title_text="Distribucion del odometro",
        xaxis_title="Odometro",
        yaxis_title="Cantidad de anuncios",
    )
    st.plotly_chart(fig, width="stretch")

if scatter_button:
    st.write(
        "Creacion de un grafico de dispersion para comparar odometro y precio."
    )
    scatter_data = car_data.dropna(subset=["odometer", "price"])
    fig = go.Figure(
        data=[
            go.Scatter(
                x=scatter_data["odometer"],
                y=scatter_data["price"],
                mode="markers",
                marker={"opacity": 0.35, "size": 6},
            )
        ]
    )
    fig.update_layout(
        title_text="Relacion entre odometro y precio",
        xaxis_title="Odometro",
        yaxis_title="Precio",
    )
    st.plotly_chart(fig, width="stretch")
