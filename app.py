import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="TripleTen EDA",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TripleTen EDA")
st.write("Base inicial para explorar datos con pandas, Plotly y Streamlit.")

uploaded_file = st.file_uploader("Carga un archivo CSV", type=["csv"])

if uploaded_file is None:
    st.info("Cuando tengamos el dataset, cargalo aqui para empezar el analisis.")
    st.stop()

df = pd.read_csv(uploaded_file)

st.subheader("Vista previa")
st.dataframe(df.head(), use_container_width=True)

st.subheader("Resumen")
st.write(df.describe(include="all"))

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if numeric_columns:
    selected_column = st.selectbox("Selecciona una columna numerica", numeric_columns)
    fig = px.histogram(df, x=selected_column, title=f"Distribucion de {selected_column}")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("El archivo no contiene columnas numericas para graficar.")
