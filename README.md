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

## Estructura inicial

- `app.py`: aplicacion Streamlit inicial.
- `requirements.txt`: dependencias minimas del proyecto.
- `data/`: carpeta para guardar datasets locales.

Los archivos de datos se ignoran en Git para evitar subir datasets pesados o
privados por accidente.
