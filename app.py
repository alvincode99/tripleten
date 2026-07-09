from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DATA_PATH = Path("data/vehicles_us.csv")
PAGE_TITLE = "Dashboard de anuncios de coches usados"

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


@dataclass(frozen=True)
class FilterSettings:
    """Valores seleccionados por la persona usuaria en la barra lateral."""

    model_year_range: tuple[int, int]
    price_range: tuple[int, int]
    vehicle_types: list[str]
    conditions: list[str]
    only_4wd: bool


st.set_page_config(
    page_title="TripleTen EDA",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_project_data(path: Path) -> pd.DataFrame:
    """Lee el CSV local del proyecto y cachea el resultado para Streamlit."""

    data = pd.read_csv(path)
    return prepare_data(data)


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """Normaliza tipos de datos usados por filtros, metricas y graficas."""

    prepared_data = data.copy()

    if "date_posted" in prepared_data:
        prepared_data["date_posted"] = pd.to_datetime(
            prepared_data["date_posted"], errors="coerce"
        )

    return prepared_data


def validate_columns(data: pd.DataFrame) -> None:
    """Detiene la app si el dataset no tiene las columnas esperadas."""

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)

    if missing_columns:
        st.error(
            "El dataset no contiene las columnas esperadas: "
            f"{', '.join(sorted(missing_columns))}"
        )
        st.stop()


def load_data_source() -> pd.DataFrame:
    """Carga el dataset versionado o permite subir un CSV alternativo."""

    if DATA_PATH.exists():
        st.caption(f"Dataset cargado: {DATA_PATH}")
        return load_project_data(DATA_PATH)

    uploaded_file = st.file_uploader("Carga un archivo CSV", type=["csv"])

    if uploaded_file is None:
        st.info("Coloca el dataset en data/vehicles_us.csv o carga un CSV.")
        st.stop()

    return prepare_data(pd.read_csv(uploaded_file))


def format_number(value: float) -> str:
    """Da formato legible a numeros usados en metricas del dashboard."""

    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def build_sidebar_filters(data: pd.DataFrame) -> FilterSettings:
    """Crea filtros interactivos y devuelve los valores seleccionados."""

    st.sidebar.header("Filtros")

    year_min = int(data["model_year"].dropna().min())
    year_max = int(data["model_year"].dropna().max())
    model_year_range = st.sidebar.slider(
        "Ano del modelo",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    price_min = int(data["price"].dropna().min())
    price_max = int(data["price"].dropna().max())
    price_range = st.sidebar.slider(
        "Precio",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
    )

    type_options = sorted(data["type"].dropna().unique())
    vehicle_types = st.sidebar.multiselect(
        "Tipo de vehiculo",
        options=type_options,
        default=type_options,
    )

    condition_options = sorted(data["condition"].dropna().unique())
    conditions = st.sidebar.multiselect(
        "Condicion",
        options=condition_options,
        default=condition_options,
    )

    only_4wd = st.sidebar.checkbox("Mostrar solo 4WD")

    return FilterSettings(
        model_year_range=model_year_range,
        price_range=price_range,
        vehicle_types=vehicle_types,
        conditions=conditions,
        only_4wd=only_4wd,
    )


def filter_data(data: pd.DataFrame, filters: FilterSettings) -> pd.DataFrame:
    """Aplica filtros de ano, precio, tipo, condicion y traccion 4WD."""

    filtered_data = data[
        data["model_year"].between(
            filters.model_year_range[0], filters.model_year_range[1]
        )
        & data["price"].between(filters.price_range[0], filters.price_range[1])
        & data["type"].isin(filters.vehicle_types)
        & data["condition"].isin(filters.conditions)
    ].copy()

    if filters.only_4wd:
        filtered_data = filtered_data[filtered_data["is_4wd"] == 1]

    return filtered_data


def render_metrics(data: pd.DataFrame) -> None:
    """Muestra indicadores generales del subconjunto filtrado."""

    metric_columns = st.columns(4)
    metric_columns[0].metric("Anuncios", format_number(len(data)))
    metric_columns[1].metric("Precio mediano", f"${format_number(data['price'].median())}")
    metric_columns[2].metric("Odometro mediano", format_number(data["odometer"].median()))
    metric_columns[3].metric("Modelos", format_number(data["model"].nunique()))


def render_data_tables(data: pd.DataFrame) -> None:
    """Muestra la vista previa y el resumen estadistico del dataset filtrado."""

    st.header("Vista previa del conjunto de datos")
    st.dataframe(data.head(20), width="stretch")

    st.header("Resumen estadistico")
    st.dataframe(data.describe(include="all").astype(str), width="stretch")


def build_histogram(data: pd.DataFrame) -> go.Figure:
    """Construye un histograma de la columna odometer."""

    fig = go.Figure(data=[go.Histogram(x=data["odometer"], nbinsx=50)])
    fig.update_layout(
        title_text="Distribucion del odometro",
        xaxis_title="Odometro",
        yaxis_title="Cantidad de anuncios",
        bargap=0.05,
    )
    return fig


def build_scatter_plot(data: pd.DataFrame) -> go.Figure:
    """Construye un grafico de dispersion entre odometer y price."""

    scatter_data = data.dropna(subset=["odometer", "price"])
    fig = go.Figure(
        data=[
            go.Scatter(
                x=scatter_data["odometer"],
                y=scatter_data["price"],
                mode="markers",
                text=scatter_data["model"],
                customdata=scatter_data[["condition", "type", "model_year"]],
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
                    "Condicion: %{customdata[0]}<br>"
                    "Tipo: %{customdata[1]}<br>"
                    "Ano: %{customdata[2]}<br>"
                    "Odometro: %{x:,.0f}<br>"
                    "Precio: $%{y:,.0f}<extra></extra>"
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


def render_visualizations(data: pd.DataFrame) -> None:
    """Renderiza los controles y graficas interactivas del dashboard."""

    st.header("Visualizaciones")
    st.write(
        "Usa los botones para construir graficos bajo demanda o activa las "
        "casillas para mantenerlos visibles mientras ajustas los filtros."
    )

    button_columns = st.columns(2)
    with button_columns[0]:
        hist_button = st.button("Construir histograma")
    with button_columns[1]:
        scatter_button = st.button("Construir grafico de dispersion")

    show_histogram = st.checkbox("Mostrar histograma automaticamente", value=True)
    show_scatter = st.checkbox(
        "Mostrar grafico de dispersion automaticamente", value=True
    )

    if hist_button or show_histogram:
        st.write(
            "Creacion de un histograma para el conjunto de datos de anuncios "
            "de venta de coches."
        )
        st.plotly_chart(build_histogram(data), width="stretch")

    if scatter_button or show_scatter:
        st.write(
            "Creacion de un grafico de dispersion para comparar odometro y precio."
        )
        st.plotly_chart(build_scatter_plot(data), width="stretch")


def main() -> None:
    """Orquesta el flujo completo de la aplicacion Streamlit."""

    st.title(PAGE_TITLE)
    st.write(
        "Explora el dataset de vehiculos usados con filtros, metricas rapidas "
        "y visualizaciones interactivas creadas con Plotly."
    )

    car_data = load_data_source()
    validate_columns(car_data)

    filters = build_sidebar_filters(car_data)
    filtered_data = filter_data(car_data, filters)

    if filtered_data.empty:
        st.warning("No hay anuncios que coincidan con los filtros seleccionados.")
        st.stop()

    render_metrics(filtered_data)
    render_data_tables(filtered_data)
    render_visualizations(filtered_data)


if __name__ == "__main__":
    main()
