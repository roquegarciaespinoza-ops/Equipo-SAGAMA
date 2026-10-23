# SAGAMA | Dashboard de evaluación y validación

Aplicación académica en Streamlit que presenta las métricas documentadas del reporte V3 del mini-hackatón sobre clasificación de diabetes (Pima Indians Diabetes).

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar desde GitHub

1. Subir `app.py` y `requirements.txt` a la raíz del repositorio.
2. Acceder a https://share.streamlit.io/ con GitHub.
3. Crear una aplicación seleccionando el repositorio, rama `main` y archivo principal `app.py`.
4. Copiar el enlace público generado a este README.

## Alcance

Las métricas son resúmenes documentados del reporte técnico. No se vuelve a entrenar el modelo ni se calculan curvas ROC a partir de probabilidades no disponibles. No es una herramienta de diagnóstico clínico.

**Resultado:** recall 83.33%, especificidad 69.00% en test; no se cumple simultáneamente el objetivo SMART.
