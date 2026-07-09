# TripleTen

Proyecto base para desarrollar un analisis exploratorio de datos con Python,
pandas, Plotly y Streamlit.

## Entorno virtual

El entorno virtual local se llama `vehicles_env`.

```bash
python3 -m venv vehicles_env
source vehicles_env/bin/activate
pip install -r requirements.txt
```

## Ejecutar la aplicacion

```bash
streamlit run app.py
```

## Notebook de analisis

El analisis exploratorio inicial esta en:

```text
notebooks/EDA.ipynb
```

Abre este notebook en VS Code y ejecuta las celdas para revisar la carga del
dataset y las visualizaciones iniciales con Plotly.

## Dataset

El conjunto de datos principal del proyecto esta en:

```text
data/vehicles_us.csv
```

Fuente original:
https://practicum-content.s3.us-west-1.amazonaws.com/new-markets/Data_sprint_4_Refactored/vehicles_us.csv

## Estructura inicial

- `app.py`: aplicacion Streamlit inicial.
- `requirements.txt`: dependencias minimas del proyecto.
- `data/`: carpeta para guardar datasets locales.
- `docs/dataset.md`: nota con la fuente del dataset.
- `notebooks/EDA.ipynb`: notebook de analisis exploratorio de datos.

Los archivos de datos se ignoran en Git por defecto para evitar subir datasets
pesados o privados por accidente. La excepcion es `data/vehicles_us.csv`,
porque es el dataset publico usado en este proyecto.
