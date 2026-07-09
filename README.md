# TripleTen

Proyecto de analisis exploratorio de datos sobre anuncios de coches usados en
Estados Unidos. El objetivo es practicar un flujo completo de trabajo con
Python: cargar un CSV, explorarlo en un notebook, construir visualizaciones con
Plotly y convertir los hallazgos iniciales en una aplicacion web con Streamlit.

La aplicacion funciona como un dashboard interactivo. Permite filtrar anuncios
por ano del modelo, precio, tipo de vehiculo, condicion y traccion 4WD; muestra
metricas rapidas del subconjunto filtrado; presenta una vista previa de los
datos; y genera visualizaciones interactivas para explorar patrones.

Funcionalidades principales:

- Filtros laterales para enfocar el analisis.
- Metricas de anuncios, precio mediano, odometro mediano y modelos unicos.
- Tabla de vista previa y resumen estadistico.
- Boton `Construir histograma` para revisar la distribucion de `odometer`.
- Boton `Construir grafico de dispersion` para comparar `odometer` contra
  `price`.
- Casillas opcionales para mantener ambas visualizaciones visibles mientras se
  cambian los filtros.

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

Despues de ejecutar el comando, abre la URL local que muestra Streamlit,
normalmente:

```text
http://localhost:8501
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

- `app.py`: dashboard Streamlit del proyecto.
- `requirements.txt`: dependencias minimas del proyecto.
- `data/`: carpeta para guardar datasets locales.
- `docs/dataset.md`: nota con la fuente del dataset.
- `notebooks/EDA.ipynb`: notebook de analisis exploratorio de datos.

Los archivos de datos se ignoran en Git por defecto para evitar subir datasets
pesados o privados por accidente. La excepcion es `data/vehicles_us.csv`,
porque es el dataset publico usado en este proyecto.
