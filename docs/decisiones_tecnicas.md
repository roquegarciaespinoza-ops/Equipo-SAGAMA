# Decisiones técnicas — Equipo SAGAMA

## DT-001: Selección de regresión logística como modelo principal

**Estado:** seleccionada como candidata principal para el mini-hackatón; no validada para uso clínico.

### Alternativas evaluadas

| Modelo | Accuracy media CV | Recall medio CV | AUC media CV |
|---|---:|---:|---:|
| Baseline (clase mayoritaria) | 0.651 | 0.000 | 0.500 |
| Regresión logística | **0.788** | 0.575 | **0.843** |
| Random Forest | 0.767 | **0.580** | 0.831 |

### Decisión y justificación

**Usaremos regresión logística como modelo principal de trabajo.** Entre los candidatos probados, tuvo la mayor AUC media en validación cruzada (0.843 frente a 0.831 de Random Forest) y mayor accuracy media (0.788 frente a 0.767). Además, es un modelo relativamente interpretable y constituye una referencia apropiada para clasificación binaria. Random Forest tuvo un recall medio ligeramente superior (0.580 frente a 0.575), por lo que no puede afirmarse que la regresión logística sea superior en todas las métricas. La diferencia de AUC tampoco demuestra por sí sola superioridad estadística.

### Umbral de decisión

Se seleccionó **0.28** usando predicciones *out-of-fold* (OOF) del entrenamiento para priorizar sensibilidad; no se eligió sobre el conjunto de test. Comparación observada en test (154 casos):

| Indicador | Umbral 0.50 | Umbral 0.28 |
|---|---:|---:|
| Recall | 0.500 | **0.833** |
| Especificidad | **0.820** | 0.670 |
| Falsos negativos | 27 | **9** |
| Falsos positivos | **18** | 33 |
| Accuracy | 0.708 | 0.727 |

La reducción de **18 falsos negativos** implica **15 falsos positivos adicionales**. La prueba de McNemar exacta reportó p=0.7283; no detectar diferencia significativa de exactitud no equivale a demostrar equivalencia.

### Evaluación contra el objetivo SMART

- Recall ≥ 80 %: **cumplido en test** (83.3 %).
- Especificidad ≥ 70 %: **no cumplido en test** (67.0 %).
- El objetivo requiere evaluación mediante validación cruzada; estos valores de test no bastan para demostrar cumplimiento en CV.

**Próxima decisión:** explorar umbrales cercanos y comprobar con predicciones OOF y evaluación apropiada si existe una configuración que alcance ambas metas. Si no existe, reportar el incumplimiento y el compromiso entre métricas, sin alterar ni maquillar resultados.

### Limitaciones

El dataset Pima representa una población específica. Faltan validación externa, análisis de subgrupos y calibración antes de considerar cualquier aplicación clínica. El sistema es exclusivamente académico y no debe usarse para diagnóstico.

## Contribuciones

Registrar aquí participantes, fecha y responsables de cada decisión. El equipo documentará rotación Driver/Navigator y commits individuales.
