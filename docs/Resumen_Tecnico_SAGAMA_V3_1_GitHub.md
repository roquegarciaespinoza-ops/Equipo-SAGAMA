# SAGAMA | Resumen técnico de resultados V3.1

**Proyecto:** Evaluación y validación de modelos de clasificación en un contexto clínico  
**Datos:** Pima Indians Diabetes | 768 registros, 8 predictores y variable objetivo `Outcome`  
**Fuente de evidencia:** `Proyecto_Pima_Evaluacion_V3_1(2).ipynb`, salidas guardadas de ejecución  
**Naturaleza:** ejercicio académico de clasificación; **no** es un instrumento de diagnóstico clínico.

## Resumen ejecutivo

La versión 3.1 conserva el procedimiento predictivo de V3 y añade trazabilidad con MLflow, evaluación offline de calidad y distribuciones con Evidently, y explicabilidad con SHAP. Se seleccionó **Random Forest** (`RF_hoja5_pesobalanced`) con umbral **0.41**. En 154 observaciones de prueba obtuvo **recall 83.33%**, **especificidad 69.00%** y **AUC 0.8157**. Se cumple la meta de sensibilidad (≥80%), pero **no** la de especificidad (≥70%); el objetivo SMART conjunto **no se alcanzó** en test. La validación anidada mostró recall medio 79.42% y especificidad media 73.00%, por lo que tampoco acredita un cumplimiento estable de ambas metas.

## 1. Problema clínico y datos

El propósito es identificar casos positivos de diabetes en un ejercicio retrospectivo de clasificación. Un **falso negativo (FN)** corresponde a un caso positivo no identificado; un **falso positivo (FP)** a una alerta incorrecta. Reducir FN puede ser valioso para un escenario de detección temprana, pero elevar FP implica pruebas adicionales, costos y preocupación innecesaria. No se han estimado costos clínicos ni validado el sistema prospectivamente.

Se utilizaron 768 registros: **614 de entrenamiento** y **154 de prueba**, con separación estratificada 80/20 y semilla 42. La distribución global fue **65.1% clase 0** y **34.9% clase 1**. Los ceros fisiológicamente implausibles en glucosa, presión arterial, grosor cutáneo, insulina e IMC se transformaron en ausencias y se imputaron dentro de los pipelines para evitar fuga de información.

| Variable | Ceros tratados como ausentes (dataset completo) |
|---|---:|
| Glucose | 5 |
| BloodPressure | 35 |
| SkinThickness | 227 |
| Insulin | 374 |
| BMI | 11 |

## 2. Modelos y baseline

Se utilizó un clasificador de clase mayoritaria como referencia trivial; la **regresión logística** constituye el baseline de modelado exigido por la actividad. Se comparó con Random Forest y, en la búsqueda ampliada, con Gradient Boosting.

| Modelo | Accuracy media CV | Recall medio CV | AUC medio CV |
|---|---:|---:|---:|
| Mayoritario (Dummy) | 0.651 | 0.000 | 0.500 |
| Regresión logística | **0.788** | 0.575 | **0.843** |
| Random Forest (configuración inicial) | 0.767 | 0.580 | 0.831 |

*Esta tabla corresponde a la comparación inicial con el umbral de clasificación predeterminado; no debe confundirse con la selección ampliada de hiperparámetros y umbrales.* La regresión logística supera claramente al clasificador mayoritario, pero su recall inicial es insuficiente para el objetivo SMART.

## 3. Selección, validación cruzada y umbral

El procedimiento V3.1 comparó combinaciones de modelos, hiperparámetros y umbrales con predicciones fuera de fold (**OOF**) sobre entrenamiento. Para evaluar el procedimiento completo se aplicó validación cruzada anidada: **5 folds externos y 3 internos**. La selección final sobre entrenamiento fue `RF_hoja5_pesobalanced`, con umbral **0.41**; en OOF logró recall **80.4%** y especificidad **74.5%**. Esos valores describen la selección en entrenamiento, no un resultado independiente.

| Fold externo | Modelo elegido en ese fold | Umbral | Recall | Especificidad | AUC |
|---|---|---:|---:|---:|---:|
| 1 | RF hoja 2, balanced | 0.36 | 79.1% | 76.2% | 0.854 |
| 2 | RF hoja 2, sin pesos | 0.31 | 81.4% | 67.5% | 0.815 |
| 3 | RF hoja 10, balanced | 0.42 | 79.1% | 73.8% | 0.869 |
| 4 | RF hoja 10, sin pesos | 0.34 | 81.4% | 72.5% | 0.812 |
| 5 | RF hoja 5, balanced | 0.42 | 76.2% | 75.0% | 0.825 |
| **Media externa** | — | — | **79.42%** | **73.00%** | — |

Los modelos y umbrales elegidos cambian entre folds. El recall externo medio queda por debajo del 80% y uno de los folds presenta especificidad de 67.5%; por ello no se demuestra estabilidad suficiente para afirmar cumplimiento general del objetivo.

## 4. Matriz de confusión e interpretación

**Test, modelo final y umbral 0.41** (filas = clase real; columnas = predicción):

| | Predicción negativa | Predicción positiva |
|---|---:|---:|
| **Real negativa** | **TN = 69** | **FP = 31** |
| **Real positiva** | **FN = 9** | **TP = 45** |

Se identificaron correctamente 45 de los 54 casos positivos; 9 quedaron sin identificar. De los 100 negativos, 31 recibieron una alerta incorrecta. La especificidad es 69/100 = **69.00%**, un punto porcentual inferior al requisito.

## 5. Métricas de evaluación final

| Métrica | Resultado, umbral 0.41 | Interpretación |
|---|---:|---|
| Accuracy | 74.03% | 114/154 clasificaciones correctas |
| Precision | 59.21% | 45/76 alertas positivas fueron verdaderas |
| Recall / sensibilidad | **83.33%** | 45/54 positivos identificados |
| Especificidad | **69.00%** | 69/100 negativos identificados |
| F1 | 69.23% | Balance armónico entre precision y recall |
| ROC-AUC | **0.8157** | Capacidad de discriminación a través de umbrales |

Fórmulas: `recall = TP/(TP+FN)`, `especificidad = TN/(TN+FP)`, `precision = TP/(TP+FP)`, `accuracy = (TP+TN)/N` y `F1 = 2·precision·recall/(precision+recall)`.

## 6. Curva ROC, AUC y precision-recall

La curva ROC representa sensibilidad frente a tasa de falsos positivos al variar el umbral. El **AUC 0.8157** indica discriminación superior al azar en esta muestra; no demuestra calibración, seguridad clínica ni cumplimiento simultáneo de los objetivos. El notebook generó una visualización de ROC, curva precision-recall y matriz de confusión. Para mostrarla en GitHub debe exportarse y añadirse el archivo de imagen a `resultados/` y enlazarse desde este documento; **no se incorpora aquí una ruta de imagen no verificada**.

## 7. Ajuste de umbral y trade-offs: simulación A/B

Se compararon, sobre los **mismos 154 registros**, A = umbral 0.50 y B = umbral 0.41. Es una comparación retrospectiva pareada, **no** un ensayo clínico A/B aleatorizado.

| Indicador | A: 0.50 | B: 0.41 | Cambio B − A |
|---|---:|---:|---:|
| Accuracy | 74.68% | 74.03% | −0.65 pp |
| Precision | 63.16% | 59.21% | −3.95 pp |
| Recall | 66.67% | **83.33%** | **+16.67 pp** |
| Especificidad | 79.00% | **69.00%** | **−10.00 pp** |
| F1 | 64.86% | 69.23% | +4.37 pp |
| TN | 79 | 69 | −10 |
| FP | 21 | 31 | +10 |
| FN | 18 | 9 | −9 |
| TP | 36 | 45 | +9 |

B reduce los falsos negativos a la mitad (**18 → 9**), a cambio de **10 falsos positivos adicionales**. La prueba exacta de McNemar produjo **p = 1.00** con 10 aciertos exclusivos de A y 9 de B. No se observó diferencia estadísticamente significativa en exactitud global; esto **no** demuestra equivalencia clínica ni ausencia de diferencias en recall o especificidad.

## 8. MLOps: registro, calidad de datos y explicabilidad

### MLflow — trazabilidad

El notebook reporta instalación de **MLflow 3.17.2**, creación del experimento `SAGAMA_Pima_MLOps` y ejecución `SAGAMA_V3_1`, con identificador:

`cc8b2bb3f12f404ca526b742ed6c86a2`

El código registra semilla, modelo, umbral, configuración de validación, métricas y archivos PNG/CSV/JSON existentes al momento del registro. La ruta de tracking es **local al entorno de Colab** (`resultados_pima/mlruns`); para conservarla debe descargarse o persistirse. Los archivos generados posteriormente al run no quedan automáticamente incorporados en ese run.

### Evidently — comparación offline

Se instaló **Evidently 0.7.23** y el notebook imprimió `Reporte Evidently generado (comparación offline)`, mediante `DataDriftPreset` y `DataSummaryPreset`, guardado como HTML. **No aparece en la salida del notebook un resumen cuantitativo de pruebas de drift**, por lo que no afirmamos que exista o no drift estadísticamente significativo. Tampoco representa monitoreo temporal de producción.

La tabla descriptiva permite detectar diferencias entre train y test. Por ejemplo, los valores ausentes de **Insulin** representan **47.23%** en train y **54.55%** en test; para **SkinThickness**, **28.50%** y **33.77%**, respectivamente. Estas diferencias deben interpretarse con cautela, especialmente por el tamaño limitado de la muestra de prueba.

### SHAP — explicabilidad predictiva

Se ejecutó **SHAP 0.54.1** sobre una muestra de hasta 30 registros de test y una referencia de hasta 60 registros de entrenamiento. Las contribuciones absolutas medias fueron:

| Variable | SHAP absoluto medio |
|---|---:|
| Glucose | **0.115584** |
| BMI | **0.081322** |
| Age | **0.054869** |
| DiabetesPedigreeFunction | 0.034095 |
| Insulin | 0.031267 |
| SkinThickness | 0.017345 |
| Pregnancies | 0.015349 |
| BloodPressure | 0.009920 |

Glucosa, IMC y edad muestran la mayor contribución absoluta media en la muestra explicada. **Importancia predictiva no equivale a causalidad clínica**, y los valores dependen de la muestra, el modelo y el método de explicación.

## 9. Evaluación frente a validación e impacto en salud

**Evaluación:** la capacidad de discriminación y las métricas del modelo están documentadas. **Validación:** la estabilidad del procedimiento es limitada y la especificidad de test no alcanza la meta. La búsqueda de modelos V1–V3.1 utilizó reiteradamente la misma partición de prueba como referencia histórica; por tanto, los resultados de test deben tratarse como evidencia exploratoria, no como validación externa independiente.

La priorización del recall responde a la preocupación por falsos negativos, pero el aumento de falsos positivos puede implicar derivaciones y pruebas adicionales. El conjunto Pima corresponde a una población específica, no representa automáticamente a otros grupos y no permite concluir utilidad clínica sin validación externa, evaluación de subgrupos, calibración, análisis prospectivo y supervisión profesional.

## 10. Conclusiones y próximos pasos

1. **Objetivo SMART: no cumplido en test.** Recall 83.33% ≥80%, pero especificidad 69.00% <70%.
2. **Validación anidada:** recall externo medio 79.42% y especificidad 73.00%; el desempeño del proceso de selección no es estable en ambas metas.
3. **Trade-off cuantificado:** el umbral 0.41 reduce 9 falsos negativos frente a 0.50, pero añade 10 falsos positivos.
4. **MLOps ejecutado:** MLflow generó un run, Evidently un reporte offline y SHAP un análisis de contribuciones; estas herramientas fortalecen trazabilidad e interpretación, pero no mejoran automáticamente el desempeño.
5. **Decisión técnica:** conservar V3.1 como evidencia experimental; no ajustar el umbral usando el mismo test conocido para forzar cumplimiento. Para una afirmación de generalización se requieren datos verdaderamente independientes.

### Evidencias a conservar en el repositorio

- Notebook ejecutado `Proyecto_Pima_Evaluacion_V3_1(2).ipynb`.
- CSV de validación, evaluación, simulación A/B y calidad de datos.
- Gráficas ROC, precision-recall, matriz de confusión, dashboard y SHAP.
- Reporte HTML de Evidently y directorio de tracking MLflow si se desea conservar la trazabilidad local.
- Registro de contribuciones y revisión colaborativa mediante commits y pull requests.

### Fuentes

- Instrucciones académicas: *Mini-Hackatón, Evaluación y Validación de Modelos de Clasificación en un Contexto Clínico, Parte I* (Tecmilenio; documento proporcionado para el proyecto).
- Resultados y código: `Proyecto_Pima_Evaluacion_V3_1(2).ipynb` (ejecución compartida por el equipo SAGAMA).
- Dataset indicado en las instrucciones: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

> **Nota:** este reporte resume las salidas guardadas del notebook. La presencia de mensajes de ejecución no sustituye una auditoría independiente de los archivos exportados ni una validación clínica.
