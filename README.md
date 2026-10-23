# Equipo SAGAMA

## Mini-Hackatón: Evaluación y Validación de Modelos de Clasificación en un Contexto Clínico

**Objetivo:** predecir diabetes tipo 2 con el dataset Pima Indians Diabetes, buscando **recall ≥ 80 %** y **especificidad ≥ 70 %**, mediante validación cruzada durante una semana de experimentación.

**Dataset:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

## Definición del problema clínico (Paso 2)
El objetivo es identificar posibles casos de diabetes tipo 2 mediante variables del dataset Pima Indians Diabetes y apoyar la priorización de evaluaciones médicas. Un falso negativo puede retrasar la detección; un falso positivo puede motivar evaluaciones adicionales innecesarias. La detección temprana es relevante para la salud pública, pero estos resultados académicos no deben utilizarse para diagnóstico clínico.

**Criterio SMART:** recall ≥ 80 % y especificidad ≥ 70 %, evaluados mediante validación cruzada durante una semana de experimentación.

**Resultados observados en el Colab ejecutado:** 768 registros (614 entrenamiento, 154 prueba), regresión logística elegida por AUC media de validación cruzada (0.843), umbral 0.28 seleccionado con predicciones fuera de pliegue (OOF) sobre entrenamiento. En test: recall 83.3 %, especificidad 67.0 %, accuracy 72.7 %, AUC 0.813; matriz de confusión TN=67, FP=33, FN=9, TP=45. **Cumple recall, pero no especificidad**. Estos valores en test no demuestran cumplimiento de ambos criterios bajo validación cruzada.

Comparación A/B simulada de umbrales 0.50 y 0.28: se reducen 18 falsos negativos a cambio de 15 falsos positivos adicionales. Prueba de McNemar exacta p=0.7283; no se detectó diferencia significativa de exactitud, lo cual no demuestra equivalencia.

**Limitaciones:** dataset de población específica, sin validación externa, análisis de subgrupos ni calibración documentada. No usar como diagnóstico.

## Equipo
Equipo SAGAMA — cuatro integrantes (nombres por completar).

## Evidencia ejecutada del equipo
- [Colab ejecutado con código, salidas y conclusiones](notebooks/Proyecto_Pima_Evaluacion_ejecutado.ipynb). Archivo original proporcionado por el equipo; conservarlo como evidencia y punto de partida para los entregables.

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

**Estado:** repositorio inicial y definición clínica documentados. El notebook ejecutado original ya está incorporado con sus salidas. Pendientes: exportar artefactos independientes y completar reporte y dashboard.
