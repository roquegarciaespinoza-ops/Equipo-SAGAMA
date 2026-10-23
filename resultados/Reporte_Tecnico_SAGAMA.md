# Equipo SAGAMA | Reporte técnico de evaluación y validación

**Proyecto:** Mini-hackatón «Evaluación y Validación de Modelos de Clasificación en un Contexto Clínico»  
**Versión analizada:** Proyecto_Pima_Evaluacion_V3(1).ipynb (ejecución conservada)  
**Repositorio:** https://github.com/roquegarciaespinoza-ops/Equipo-SAGAMA  
**Dictamen:** Objetivo SMART **no cumplido simultáneamente** en test (recall 83.33%; especificidad 69.00%).

## Resumen ejecutivo

El equipo SAGAMA desarrolló un flujo de clasificación supervisada para explorar la detección de diabetes tipo 2 mediante el conjunto Pima Indians Diabetes. El proceso integra limpieza de datos, modelos clásicos, validación cruzada, selección de umbral, evaluación independiente dentro del experimento y simulación A/B. En V3 se seleccionó Random Forest con umbral 0.41. El modelo identificó 45 de 54 positivos (recall 83.33%) y 69 de 100 negativos (especificidad 69%). El objetivo de sensibilidad se alcanzó, pero la especificidad quedó un punto porcentual por debajo de la meta. La validación anidada mostró además una sensibilidad media de 79.4%, por lo que no existe evidencia robusta de cumplimiento conjunto. Este resultado debe reportarse sin redondear 69% a 70% ni presentar el modelo como herramienta clínica.

## 1. Definición del problema y contexto clínico

El problema consiste en clasificar si un registro corresponde a un resultado positivo (`Outcome=1`) o negativo (`Outcome=0`) de diabetes a partir de variables clínicas del dataset Pima: embarazos, glucosa, presión arterial, grosor del pliegue cutáneo, insulina, índice de masa corporal, función de pedigrí de diabetes y edad. El objetivo educativo es analizar el potencial de modelos predictivos como apoyo a la identificación de casos que requieren valoración adicional, no emitir diagnósticos.

El riesgo principal de un **falso negativo (FN)** es no identificar a una persona positiva en el conjunto de datos, lo que, en un contexto hipotético de tamizaje, podría retrasar una evaluación médica. Un **falso positivo (FP)** puede generar evaluaciones adicionales, costos y preocupación innecesaria. Por ello, la actividad exige simultáneamente recall ≥80% y especificidad ≥70%: no basta con detectar más positivos a costa de un volumen excesivo de falsas alarmas.

El dataset contiene 768 registros y nueve columnas (ocho predictores y el resultado). La distribución observada fue 500 negativos (65.1%) y 268 positivos (34.9%). Se reservaron 614 registros para entrenamiento y 154 para prueba, mediante partición estratificada 80/20 y semilla 42. Se trataron como ausentes los ceros fisiológicamente implausibles de glucosa (5), presión arterial (35), pliegue cutáneo (227), insulina (374) e IMC (11), imputando dentro de los pipelines para reducir fuga de información.

## 2. Matriz de confusión e interpretación

La matriz final de V3, con Random Forest y umbral 0.41, tiene filas correspondientes a la clase real y columnas a la predicción:

| Clase real / Predicción | Negativa (0) | Positiva (1) |
|---|---:|---:|
| Negativa (0) | 69 (VN) | 31 (FP) |
| Positiva (1) | 9 (FN) | 45 (VP) |

Sobre 154 observaciones, el modelo acertó 114 (69+45) y se equivocó en 40 (31+9). Los nueve falsos negativos representan casos positivos no detectados. Los 31 falsos positivos representan registros negativos señalados como positivos. Esta matriz permite verificar directamente la sensibilidad y la especificidad; no se interpreta como evidencia de utilidad clínica fuera de la muestra.

## 3. Cálculo e interpretación de métricas

Las métricas se calculan a partir de VP=45, VN=69, FP=31 y FN=9:

| Métrica | Fórmula | Resultado V3 (test) | Interpretación |
|---|---|---:|---|
| Accuracy | (VP+VN)/N | 74.03% | Proporción total de aciertos |
| Precision | VP/(VP+FP) | 59.21% | Positivos predichos que realmente son positivos |
| Recall / sensibilidad | VP/(VP+FN) | 83.33% | Positivos reales identificados; cumple ≥80% |
| Especificidad | VN/(VN+FP) | 69.00% | Negativos reales identificados; no cumple ≥70% |
| F1-score | 2·precision·recall/(precision+recall) | 69.23% | Equilibrio armónico entre precision y recall |
| ROC-AUC | Área bajo la curva ROC | 0.8157 | Discriminación global del ranking de probabilidades |

La exactitud global, por sí sola, no refleja el costo asimétrico de los errores. Por ello, la decisión se apoya principalmente en recall y especificidad, utilizando precision, F1 y AUC como métricas complementarias.

## 4. Ajuste de umbral y análisis de trade-offs

El umbral convencional 0.50 se comparó con el umbral 0.41 seleccionado en entrenamiento. Al disminuir el umbral, más registros se clasifican como positivos: aumenta la sensibilidad y disminuye la especificidad.

| Métrica | A: umbral 0.50 | B: umbral 0.41 | Diferencia B−A |
|---|---:|---:|---:|
| Recall | 66.67% | 83.33% | +16.67 puntos porcentuales |
| Especificidad | 79.00% | 69.00% | −10.00 puntos porcentuales |
| Precision | 63.16% | 59.21% | −3.95 puntos porcentuales |
| Accuracy | 74.68% | 74.03% | −0.65 puntos porcentuales |
| FN | 18 | 9 | −9 |
| FP | 21 | 31 | +10 |

En las predicciones fuera de fold (OOF) del conjunto de entrenamiento, la combinación final obtuvo recall 80.4% y especificidad 74.5%, satisfaciendo ambas restricciones en esa etapa. No obstante, en test la especificidad cayó a 69%. El umbral no debe reajustarse usando test para forzar el cumplimiento, porque eso contaminaría la evaluación. La curva precision-recall generada en el notebook documenta el comportamiento de precision y recall al cambiar el umbral.

## 5. Curva ROC y AUC

La curva ROC representa la tasa de verdaderos positivos (recall) frente a la tasa de falsos positivos (1−especificidad) para diferentes umbrales. El AUC de V3 en test fue **0.8157**, lo que indica una capacidad de discriminación superior al azar (AUC=0.50) dentro de esta muestra. El punto operativo del umbral 0.41 corresponde a FPR=0.31 y TPR=0.8333. El escenario A, umbral 0.50, corresponde a FPR=0.21 y TPR=0.6667.

El AUC no cambia entre A y B porque ambos utilizan las mismas probabilidades: solo cambia la decisión binaria. El notebook ejecutado incluye gráficas ROC, precision-recall y matriz de confusión. Para GitHub se recomienda exportarlas a `resultados/` y enlazarlas desde este informe; no se incorporan imágenes con rutas no verificadas.

## 6. Resultados de validación cruzada

Se aplicó validación cruzada estratificada de cinco folds para comparar modelos de referencia. Los resultados siguientes corresponden al umbral predeterminado de los clasificadores:

| Modelo | Accuracy media ± DE | Recall medio ± DE | AUC media ± DE |
|---|---:|---:|---:|
| Baseline mayoritario | 0.651 ± 0.002 | 0.000 ± 0.000 | 0.500 ± 0.000 |
| Regresión logística | 0.788 ± 0.021 | 0.575 ± 0.025 | 0.843 ± 0.021 |
| Random Forest | 0.767 ± 0.012 | 0.580 ± 0.046 | 0.831 ± 0.024 |

V3 añadió un procedimiento de validación anidada para estimar el comportamiento de la selección de configuración y umbral. Cada fold externo empleó una selección interna; el resultado externo fue:

| Fold externo | Modelo elegido | Umbral | Recall | Especificidad | AUC |
|---|---|---:|---:|---:|---:|
| 1 | RF hoja 2, balanced | 0.36 | 79.1% | 76.2% | 0.854 |
| 2 | RF hoja 2, sin ponderación | 0.31 | 81.4% | 67.5% | 0.815 |
| 3 | RF hoja 10, balanced | 0.42 | 79.1% | 73.8% | 0.869 |
| 4 | RF hoja 10, sin ponderación | 0.34 | 81.4% | 72.5% | 0.812 |
| 5 | RF hoja 5, balanced | 0.42 | 76.2% | 75.0% | 0.825 |
| **Media externa** | — | — | **79.4%** | **73.0%** | — |

La variación de umbrales y de configuraciones muestra sensibilidad del procedimiento a la partición. El recall externo medio no alcanza el 80%, aunque la especificidad media sí supera el 70%. Ninguno de los cinco folds externos cumplió simultáneamente ambas metas. Esta evidencia impide concluir que el cumplimiento conjunto esté validado de forma robusta.

## 7. Comparación con baseline

El baseline mayoritario predice siempre la clase negativa. Su accuracy de validación fue aproximadamente 65.1%, pero su recall fue 0%, por lo que no sirve para detectar positivos. La regresión logística —baseline de modelado exigido por el ejercicio— alcanzó AUC media de 0.843 y recall medio de 0.575 con umbral estándar; Random Forest obtuvo AUC media de 0.831 y recall medio de 0.580. Estos resultados son de la comparación inicial, no de la configuración optimizada final.

En test, la versión final V3 con Random Forest y umbral 0.41 alcanzó accuracy 74.03%, recall 83.33% y AUC 0.8157. Frente al clasificador mayoritario, aumenta la capacidad de detectar positivos a costa de falsas alarmas. Frente a los modelos clásicos iniciales, el beneficio relevante se observa al elegir el umbral con base en el objetivo operativo, no en accuracy aislada.

## 8. Análisis de pruebas A/B

La prueba A/B es **simulada y pareada**: se aplican al mismo conjunto de 154 registros las probabilidades del mismo Random Forest, cambiando únicamente el umbral (A=0.50; B=0.41). No hubo asignación aleatoria de pacientes ni intervención clínica.

El escenario B redujo los FN de 18 a 9 (nueve menos), pero aumentó los FP de 21 a 31 (diez más). La prueba exacta de McNemar comparó las discordancias de acierto: diez observaciones acertadas solo por A y nueve acertadas solo por B; 19 discordancias y **p=1.000** (α=0.05). No se detectó diferencia estadísticamente significativa de exactitud global. Este resultado no demuestra equivalencia de los escenarios ni ausencia de diferencias clínicamente relevantes en los tipos de error.

## 9. Justificación técnica y relación con impacto en salud

La solución utiliza algoritmos clásicos permitidos por el hackatón, una partición estratificada, imputación dentro de los pipelines y validación cruzada. La regresión logística ofrece interpretabilidad y un punto de comparación; Random Forest permite modelar relaciones no lineales; Gradient Boosting se consideró entre las configuraciones candidatas de V3. El modelo final fue Random Forest con cinco muestras mínimas por hoja y ponderación de clases equilibrada, seleccionado con umbral 0.41 mediante predicciones OOF de entrenamiento.

La prioridad otorgada al recall responde al costo potencial de omitir casos positivos en un escenario de tamizaje. Sin embargo, la especificidad mínima evita aceptar cualquier aumento de sensibilidad sin valorar la carga de falsas alarmas. Los resultados no representan sensibilidad o especificidad poblacional, porque el dataset es pequeño, corresponde a una población específica y no cuenta aquí con validación externa, evaluación prospectiva ni análisis completo de subgrupos y calibración. El modelo es **un prototipo académico**, no un dispositivo diagnóstico ni una herramienta aprobada para uso sanitario.

Desde la gestión de proyectos de IA, la evaluación cuantifica métricas; la validación determina si el procedimiento mantiene desempeño, satisface restricciones y permite una decisión responsable. La discrepancia entre OOF, validación anidada y test es una señal que debe investigarse y documentarse, no ocultarse.

## 10. Conclusiones

El proyecto implementó un flujo reproducible de experimentación con 768 registros, evaluación de modelos clásicos, selección de umbral, curvas ROC/precision-recall, validación cruzada anidada y simulación A/B. V3 mejoró el equilibrio observado frente a versiones anteriores: mantuvo 45 verdaderos positivos y nueve falsos negativos, mientras redujo falsos positivos respecto de V1 (33) y V2 (35) hasta 31. Sin embargo, en test obtuvo recall 83.33% y especificidad 69.00%; **no cumplió simultáneamente el objetivo SMART**. La validación anidada también arrojó recall externo medio de 79.4%, por debajo de la meta.

La conclusión central es que mejorar una métrica no equivale a validar una solución. El trabajo demuestra una capacidad predictiva útil para la discusión académica, pero evidencia limitaciones de generalización y de equilibrio entre errores. Recomendamos conservar V3 como resultado experimental documentado, no continuar ajustando el mismo test, verificar reproducibilidad y evaluar con datos externos si el proyecto evoluciona hacia un contexto real. La decisión responsable es reconocer el cumplimiento parcial y explicar sus causas, en lugar de declarar éxito únicamente por superar el 80% de sensibilidad.

## Fuentes y trazabilidad

- Tecmilenio. *Mini-hackatón: Evaluación y Validación de Modelos de Clasificación en un Contexto Clínico, Parte I*. Instrucciones proporcionadas para la actividad.
- Equipo SAGAMA. *Proyecto_Pima_Evaluacion_V3(1).ipynb*. Notebook ejecutado, fuente de tablas, matrices y resultados V3.
- Equipo SAGAMA. *Proyecto_Pima_Evaluacion.ipynb* y *Proyecto_Pima_Evaluacion V2.ipynb*. Resultados históricos V1 y V2.
- UCI / Kaggle. *Pima Indians Diabetes Database*. https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
- Repositorio del equipo: https://github.com/roquegarciaespinoza-ops/Equipo-SAGAMA

> **Nota de publicación:** incorporar las gráficas exportadas desde el notebook y verificar el historial de contribuciones del equipo antes de entregar el repositorio. Este informe no afirma que se haya realizado validación clínica externa.
