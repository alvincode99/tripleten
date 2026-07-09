from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DATA_PATH = Path("data/vehicles_us.csv")
REQUIRED_COLUMNS = {
    "price",
    "model_year",
    "model",
    "condition",
    "odometer",
    "type",
    "is_4wd",
    "date_posted",
}


st.set_page_config(
    page_title="TripleTen EDA",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_project_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["date_posted"] = pd.to_datetime(data["date_posted"], errors="coerce")
    return data


def format_number(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def build_histogram(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Histogram(x=data["odometer"], nbinsx=50)])
    fig.update_layout(
        title_text="Distribucion del odometro",
        xaxis_title="Odometro",
        yaxis_title="Cantidad de anuncios",
        bargap=0.05,
    )
    return fig


def build_scatter_plot(data: pd.DataFrame) -> go.Figure:
    scatter_data = data.dropna(subset=["odometer", "price"])
    fig = go.Figure(
        data=[
            go.Scatter(
                x=scatter_data["odometer"],
                y=scatter_data["price"],
                mode="markers",
                text=scatter_data["model"],
                marker={
                    "opacity": 0.4,
                    "size": 7,
                    "color": scatter_data["model_year"],
                    "colorscale": "Viridis",
                    "showscale": True,
                    "colorbar": {"title": "Ano"},
                },
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Odometro: %{x:,.0f}<br>"
                    "Precio: $%{y:,.0f}<br>"
                    "Ano: %{marker.color}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title_text="Relacion entre odometro y precio",
        xaxis_title="Odometro",
        yaxis_title="Precio",
    )
    return fig


st.title("Dashboard de anuncios de coches usados")
st.write(
    "Explora el dataset de vehiculos usados con filtros, metricas rapidas y "
    "visualizaciones interactivas creadas con Plotly."
)

if DATA_PATH.exists():
    car_data = load_project_data(DATA_PATH)
    st.caption(f"Dataset cargado: {DATA_PATH}")
else:
    uploaded_file = st.file_uploader("Carga un archivo CSV", type=["csv"])

    if uploaded_file is None:
        st.info("Coloca el dataset en data/vehicles_us.csv o carga un CSV.")
        st.stop()

    car_data = pd.read_csv(uploaded_file)
    if "date_posted" in car_data:
        car_data["date_posted"] = pd.to_datetime(
            car_data["date_posted"], errors="coerce"
        )

missing_columns = REQUIRED_COLUMNS.difference(car_data.columns)

if missing_columns:
    st.error(
        "El dataset no contiene las columnas esperadas: "
        f"{', '.join(sorted(missing_columns))}"
    )
    st.stop()

st.sidebar.header("Filtros")

year_min = int(car_data["model_year"].dropna().min())
year_max = int(car_data["model_year"].dropna().max())
selected_years = st.sidebar.slider(
    "Ano del modelo",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

price_min = int(car_data["price"].dropna().min())
price_max = int(car_data["price"].dropna().max())
selected_prices = st.sidebar.slider(
    "Precio",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
)

type_options = sorted(car_data["type"].dropna().unique())
selected_types = st.sidebar.multiselect(
    "Tipo de vehiculo",
    options=type_options,
    default=type_options,
)

condition_options = sorted(car_data["condition"].dropna().unique())
selected_conditions = st.sidebar.multiselect(
    "Condicion",
    options=condition_options,
    default=condition_options,
)

only_4wd = st.sidebar.checkbox("Mostrar solo 4WD")

filtered_data = car_data[
    car_data["model_year"].between(selected_years[0], selected_years[1])
    & car_data["price"].between(selected_prices[0], selected_prices[1])
    & car_data["type"].isin(selected_types)
    & car_data["condition"].isin(selected_conditions)
].copy()

if only_4wd:
    filtered_data = filtered_data[filtered_data["is_4wd"] == 1]

if filtered_data.empty:
    st.warning("No hay anuncios que coincidan con los filtros seleccionados.")
    st.stop()

metric_columns = st.columns(4)
metric_columns[0].metric("Anuncios", format_number(len(filtered_data)))
metric_columns[1].metric(
    "Precio mediano",
    f"${format_number(filtered_data['price'].median())}",
)
metric_columns[2].metric(
    "Odometro mediano",
    format_number(filtered_data["odometer"].median()),
)
metric_columns[3].metric("Modelos", format_number(filtered_data["model"].nunique()))

st.header("Vista previa del conjunto de datos")
st.dataframe(filtered_data.head(20), width="stretch")

st.header("Resumen estadistico")
st.dataframe(filtered_data.describe(include="all").astype(str), width="stretch")

st.header("Visualizaciones")
st.write(
    "Usa los botones para construir graficos bajo demanda o activa las casillas "
    "para mantenerlos visibles mientras ajustas los filtros."
)

button_columns = st.columns(2)
with button_columns[0]:
    hist_button = st.button("Construir histograma")
with button_columns[1]:
    scatter_button = st.button("Construir grafico de dispersion")

show_histogram = st.checkbox("Mostrar histograma automaticamente", value=True)
show_scatter = st.checkbox("Mostrar grafico de dispersion automaticamente", value=True)

if hist_button or show_histogram:
    st.write(
        "Creacion de un histograma para el conjunto de datos de anuncios de "
        "venta de coches."
    )
    st.plotly_chart(build_histogram(filtered_data), width="stretch")

if scatter_button or show_scatter:
    st.write(
        "Creacion de un grafico de dispersion para comparar odometro y precio."
    )
    st.plotly_chart(build_scatter_plot(filtered_data), width="stretch")
