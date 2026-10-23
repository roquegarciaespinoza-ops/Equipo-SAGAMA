# Equipo SAGAMA

## Mini-Hackatón: Evaluación y Validación de Modelos de Clasificación en un Contexto Clínico

**Objetivo:** predecir diabetes tipo 2 con el dataset Pima Indians Diabetes, buscando **recall ≥ 80 %** y **especificidad ≥ 70 %**, mediante validación cruzada durante una semana de experimentación.

**Dataset:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

## Definición del problema clínico
Se busca identificar casos positivos de diabetes tipo 2 a partir de las variables disponibles. Los falsos negativos pueden retrasar la detección y los falsos positivos pueden ocasionar pruebas adicionales. Este proyecto es académico y no constituye una herramienta clínica validada.

## Equipo
Equipo SAGAMA — cuatro integrantes (nombres por completar).

## Estructura
- `data/`: instrucciones para obtener el dataset.
- `notebooks/exploracion.ipynb`: carga, estadísticas, distribuciones y desbalance.
- `notebooks/modelo.ipynb`: baseline, métricas, validación cruzada, ajuste de umbral, ROC/AUC.
- `notebooks/pruebas_ab.ipynb`: simulación de umbral 0.50 contra umbral optimizado.
- `dashboard/`: tablero visual.
- `resultados/graficas/` y `resultados/metricas/`: evidencias.
- `docs/decisiones_tecnicas.md`: decisiones del equipo.

## Reporte técnico (por completar)
1. Definición del problema y contexto clínico.
2. Matriz de confusión e interpretación.
3. Cálculo e interpretación de accuracy, precision, recall, F1 y especificidad.
4. Ajuste de umbral y análisis de trade-offs.
5. Curva ROC y AUC.
6. Resultados de validación cruzada (k=5 o 10).
7. Comparación con baseline de regresión logística.
8. Análisis de pruebas A/B simuladas.
9. Justificación técnica e impacto en salud.
10. Conclusiones y recomendaciones.

## Contribuciones del equipo y dinámica de trabajo
Registrar aquí los nombres, responsabilidades y contribuciones de los cuatro integrantes. Realizar pair programming con roles Driver y Navigator alternados cada 20–30 minutos. Cada participante debe aportar commits y documentar decisiones técnicas.

## Entregas
- **Día 1:** repositorio, problema clínico y notebooks.
- **Día 2:** dashboard y reporte técnico en README.

## Preparación
Instalar dependencias con `pip install -r requirements.txt`, descargar el dataset y guardarlo localmente en `data/diabetes.csv`.

**Estado:** estructura inicial. Aún no se han ejecutado experimentos ni calculado resultados.
