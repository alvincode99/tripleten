# TripleTen

Proyecto de analisis exploratorio de datos sobre anuncios de coches usados en
Estados Unidos. El trabajo combina un notebook de exploracion con una aplicacion
web hecha en Streamlit para convertir el analisis inicial en un dashboard
interactivo.

## Objetivo del proyecto

El objetivo principal es practicar un flujo de trabajo completo de analisis de
datos con Python:

1. Crear y configurar un entorno virtual.
2. Instalar las dependencias necesarias: pandas, Plotly y Streamlit.
3. Descargar y guardar el dataset `vehicles_us.csv` dentro del proyecto.
4. Explorar el dataset en un Jupyter Notebook.
5. Construir visualizaciones interactivas con Plotly.
6. Desarrollar una aplicacion web con Streamlit.
7. Versionar y publicar el proyecto en GitHub.

## Descripcion de la aplicacion

La aplicacion web funciona como un dashboard EDA para revisar anuncios de venta
de coches usados. Permite explorar el dataset sin modificar el archivo original
y ofrece controles interactivos para enfocar el analisis en subconjuntos
especificos.

Funcionalidades incluidas:

- Carga automatica del dataset `data/vehicles_us.csv`.
- Validacion de columnas esperadas antes de ejecutar el dashboard.
- Filtros laterales por ano del modelo, precio, tipo de vehiculo, condicion y
  traccion 4WD.
- Metricas rapidas sobre el subconjunto filtrado:
  - cantidad de anuncios;
  - precio mediano;
  - odometro mediano;
  - cantidad de modelos unicos.
- Vista previa de las primeras filas filtradas.
- Resumen estadistico del subconjunto activo.
- Boton `Construir histograma` para visualizar la distribucion de `odometer`.
- Boton `Construir grafico de dispersion` para comparar `odometer` contra
  `price`.
- Casillas de verificacion para mantener visibles las visualizaciones mientras
  se cambian los filtros.

## Dataset

El conjunto de datos principal esta guardado en:

```text
data/vehicles_us.csv
```

Fuente original:
https://practicum-content.s3.us-west-1.amazonaws.com/new-markets/Data_sprint_4_Refactored/vehicles_us.csv

El dataset contiene `51,525` anuncios y `13` columnas:

- `price`: precio anunciado del vehiculo.
- `model_year`: ano del modelo.
- `model`: modelo del vehiculo.
- `condition`: condicion reportada.
- `cylinders`: numero de cilindros.
- `fuel`: tipo de combustible.
- `odometer`: lectura del odometro.
- `transmission`: tipo de transmision.
- `type`: categoria del vehiculo.
- `paint_color`: color.
- `is_4wd`: indicador de traccion 4WD.
- `date_posted`: fecha de publicacion del anuncio.
- `days_listed`: dias que el anuncio estuvo listado.

## Estructura del proyecto

```text
.
|-- app.py
|-- data/
|   |-- .gitkeep
|   `-- vehicles_us.csv
|-- docs/
|   `-- dataset.md
|-- notebooks/
|   `-- EDA.ipynb
|-- requirements.txt
`-- README.md
```

Descripcion de archivos principales:

- `app.py`: aplicacion Streamlit del dashboard.
- `notebooks/EDA.ipynb`: notebook de analisis exploratorio inicial.
- `data/vehicles_us.csv`: dataset del proyecto.
- `docs/dataset.md`: nota con la fuente y ubicacion del dataset.
- `requirements.txt`: dependencias necesarias para ejecutar el proyecto.
- `.gitignore`: exclusiones para entorno virtual, cache y datasets no
  versionados.

## Entorno virtual

El entorno virtual local se llama `vehicles_env`.

Crear el entorno:

```bash
python3 -m venv vehicles_env
```

Activarlo:

```bash
source vehicles_env/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Dependencias principales:

- `pandas`: lectura y transformacion del CSV.
- `plotly`: graficas interactivas.
- `streamlit`: aplicacion web.

## Ejecutar la aplicacion

Desde la raiz del proyecto, ejecuta:

```bash
streamlit run app.py
```

Despues abre la URL local que muestra Streamlit. Normalmente sera:

```text
http://localhost:8501
```

## Notebook de analisis

El notebook esta en:

```text
notebooks/EDA.ipynb
```

El notebook incluye:

- carga del dataset con pandas;
- revision de dimensiones y columnas;
- revision de valores nulos;
- resumen estadistico;
- histograma de la columna `odometer`;
- grafico de dispersion `odometer` vs `price`;
- boxplot de `price` por `condition`.

## Detalle del codigo de `app.py`

El archivo `app.py` esta organizado en funciones para que el flujo sea claro:

- `load_project_data()`: carga el CSV local y cachea el resultado con
  `st.cache_data`.
- `prepare_data()`: convierte `date_posted` a tipo fecha cuando la columna
  existe.
- `validate_columns()`: revisa que el dataset tenga las columnas necesarias.
- `load_data_source()`: usa `data/vehicles_us.csv` o permite subir un CSV si el
  archivo local no existe.
- `build_sidebar_filters()`: crea los filtros de la barra lateral.
- `filter_data()`: aplica los filtros al DataFrame.
- `render_metrics()`: muestra las metricas principales.
- `render_data_tables()`: muestra la vista previa y el resumen estadistico.
- `build_histogram()`: construye el histograma de `odometer`.
- `build_scatter_plot()`: construye el grafico de dispersion entre `odometer` y
  `price`.
- `render_visualizations()`: muestra botones, casillas y graficas.
- `main()`: coordina todo el flujo de la aplicacion.

## Flujo de uso recomendado

1. Activar el entorno virtual.
2. Instalar dependencias si todavia no estan instaladas.
3. Abrir `notebooks/EDA.ipynb` para revisar el analisis inicial.
4. Ejecutar `streamlit run app.py`.
5. Ajustar filtros en la barra lateral.
6. Usar los botones o casillas para construir las visualizaciones.

## Validaciones realizadas

Durante el desarrollo se verifico que:

- el CSV se lee correctamente con pandas;
- el notebook `EDA.ipynb` es JSON valido;
- `app.py` compila sin errores de sintaxis;
- la app de Streamlit carga sin excepciones;
- los botones de histograma y dispersion funcionan;
- las casillas opcionales se renderizan correctamente;
- la aplicacion responde localmente en `http://localhost:8501`;
- los cambios fueron confirmados y enviados al repositorio remoto en GitHub.

## Repositorio

Repositorio publico:

```text
https://github.com/alvincode99/tripleten
```

Rama principal:

```text
main
```

## Notas

Los archivos de datos se ignoran en Git por defecto para evitar subir datasets
pesados o privados por accidente. La excepcion es `data/vehicles_us.csv`, porque
es el dataset publico usado en este proyecto.
