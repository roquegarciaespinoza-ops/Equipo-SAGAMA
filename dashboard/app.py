import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='SAGAMA | Evaluación de modelos', page_icon='📊', layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem}.subtle{color:#63758a;font-size:.94rem}.note{padding:1rem;border-left:4px solid #e4a340;background:#fff7e9;color:#493800;border-radius:6px}</style>''', unsafe_allow_html=True)
st.title('📊 Equipo SAGAMA | Evaluación y validación')
st.caption('Mini-hackatón · Pima Indians Diabetes · Random Forest V3 · Dashboard académico')
st.info('**Dictamen:** objetivo SMART no cumplido simultáneamente en test. Recall 83.33% (meta ≥80%); especificidad 69.00% (meta ≥70%).')

A={'umbral':0.50,'recall':66.67,'especificidad':79.00,'precision':63.16,'accuracy':74.68,'FN':18,'FP':21,'VP':36,'VN':79}
B={'umbral':0.41,'recall':83.33,'especificidad':69.00,'precision':59.21,'accuracy':74.03,'FN':9,'FP':31,'VP':45,'VN':69}

with st.sidebar:
    st.header('Navegación')
    section=st.radio('Sección', ['Resumen ejecutivo','Matriz de confusión','Comparación A/B','Validación cruzada','Conclusiones y fuentes'])
    st.divider()
    st.caption('Fuente: reporte técnico SAGAMA, notebook Proyecto_Pima_Evaluacion_V3(1).ipynb. Datos resumidos documentados, no predicciones nuevas.')

if section=='Resumen ejecutivo':
    st.subheader('Desempeño del modelo final en test')
    cols=st.columns(5)
    for col,(lab,val) in zip(cols,[('Accuracy','74.03%'),('Recall','83.33%'),('Especificidad','69.00%'),('F1-score','69.23%'),('ROC-AUC','0.8157')]):
        col.metric(lab,val)
    st.markdown('**Configuración:** Random Forest · umbral 0.41 · partición estratificada 80/20 · semilla 42')
    st.markdown('**Dataset:** 768 registros (500 negativos, 268 positivos); 614 para entrenamiento y 154 para test.')
    goals=pd.DataFrame({'Métrica':['Recall','Especificidad'],'Resultado':[83.33,69.0],'Meta':[80,70]})
    fig=go.Figure()
    fig.add_bar(x=goals['Métrica'],y=goals['Resultado'],name='Resultado (%)',marker_color='#14699a',text=[f'{x:.2f}%' for x in goals['Resultado']],textposition='outside')
    fig.add_scatter(x=goals['Métrica'],y=goals['Meta'],mode='markers',name='Meta mínima (%)',marker=dict(color='#e0a02e',size=16,symbol='line-ew',line=dict(width=3)))
    fig.update_layout(title='Objetivos SMART: resultado frente a meta',yaxis_title='Porcentaje',yaxis_range=[0,105])
    st.plotly_chart(fig,use_container_width=True)
    st.warning('Cumplimiento parcial: sensibilidad suficiente, especificidad un punto porcentual por debajo de la meta. No es una herramienta clínica.')

elif section=='Matriz de confusión':
    st.subheader('Matriz de confusión — test, umbral 0.41')
    mat=[[69,31],[9,45]]
    fig=go.Figure(data=go.Heatmap(z=mat,x=['Predicho negativo (0)','Predicho positivo (1)'],y=['Real negativo (0)','Real positivo (1)'],colorscale='Blues',showscale=False,text=mat,texttemplate='%{text}',textfont={'size':24}))
    fig.update_layout(yaxis=dict(autorange='reversed'),height=410,margin=dict(t=20))
    st.plotly_chart(fig,use_container_width=True)
    c=st.columns(4)
    for col,(lab,val) in zip(c,[('VN',69),('FP',31),('FN',9),('VP',45)]):col.metric(lab,val)
    st.caption('Filas: clase real; columnas: predicción. 154 observaciones, 114 aciertos y 40 errores.')
    st.markdown('**Interpretación:** 9 casos positivos no detectados (FN) y 31 registros negativos señalados como positivos (FP).')

elif section=='Comparación A/B':
    st.subheader('Comparación simulada y pareada de umbrales')
    selected=st.radio('Escenario', ['A · Umbral 0.50','B · Umbral 0.41'],horizontal=True)
    v=A if selected.startswith('A') else B
    cols=st.columns(4)
    for col,(lab,key) in zip(cols,[('Recall','recall'),('Especificidad','especificidad'),('Precision','precision'),('Accuracy','accuracy')]):col.metric(lab,f'{v[key]:.2f}%')
    st.caption(f"Escenario seleccionado: VP={v['VP']}, VN={v['VN']}, FP={v['FP']}, FN={v['FN']}. El selector alterna entre dos escenarios documentados; no recalcula umbrales arbitrarios.")
    labels=['Recall','Especificidad','Precision','Accuracy']
    fig=go.Figure()
    for name,data,color in [('A · 0.50',A,'#64748b'),('B · 0.41',B,'#14699a')]:
        fig.add_bar(name=name,x=labels,y=[data[k] for k in ['recall','especificidad','precision','accuracy']],marker_color=color)
    fig.update_layout(barmode='group',yaxis_title='Porcentaje',yaxis_range=[0,100])
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(pd.DataFrame({'Métrica':['Recall','Especificidad','Precision','Accuracy','Falsos negativos','Falsos positivos'],'A · 0.50':[66.67,79,63.16,74.68,18,21],'B · 0.41':[83.33,69,59.21,74.03,9,31]}),hide_index=True,use_container_width=True)
    st.info('Al pasar de A a B se reducen los FN de 18 a 9, pero aumentan los FP de 21 a 31. McNemar exacta: p = 1.000; sin diferencia estadísticamente significativa de accuracy global (α=0.05). No demuestra equivalencia.')

elif section=='Validación cruzada':
    st.subheader('Comparación de modelos (validación cruzada de 5 folds)')
    models=pd.DataFrame({'Modelo':['Baseline mayoritario','Regresión logística','Random Forest'],'Accuracy media':[.651,.788,.767],'Recall medio':[0,.575,.580],'AUC media':[.500,.843,.831]})
    metric=st.selectbox('Métrica a comparar', ['Accuracy media','Recall medio','AUC media'])
    fig=go.Figure(go.Bar(x=models['Modelo'],y=models[metric],marker_color='#14699a',text=[f'{x:.3f}' for x in models[metric]],textposition='outside'))
    fig.update_layout(yaxis_range=[0,1.05],yaxis_title=metric)
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(models,hide_index=True,use_container_width=True)
    st.subheader('Validación anidada (folds externos)')
    folds=pd.DataFrame({'Fold':[1,2,3,4,5],'Modelo':['RF hoja 2, balanced','RF hoja 2, sin ponderación','RF hoja 10, balanced','RF hoja 10, sin ponderación','RF hoja 5, balanced'],'Umbral':[.36,.31,.42,.34,.42],'Recall (%)':[79.1,81.4,79.1,81.4,76.2],'Especificidad (%)':[76.2,67.5,73.8,72.5,75.0],'AUC':[.854,.815,.869,.812,.825]})
    st.dataframe(folds,hide_index=True,use_container_width=True)
    fig2=go.Figure()
    fig2.add_scatter(x=folds['Fold'],y=folds['Recall (%)'],mode='lines+markers',name='Recall (%)')
    fig2.add_scatter(x=folds['Fold'],y=folds['Especificidad (%)'],mode='lines+markers',name='Especificidad (%)')
    fig2.add_hline(y=80,line_dash='dash',line_color='#bf7022',annotation_text='Meta recall 80%')
    fig2.add_hline(y=70,line_dash='dot',line_color='#777777',annotation_text='Meta especificidad 70%')
    fig2.update_layout(xaxis=dict(tickmode='linear',dtick=1),yaxis_title='Porcentaje',yaxis_range=[60,90])
    st.plotly_chart(fig2,use_container_width=True)
    st.warning('Medias externas reportadas: recall 79.4%, especificidad 73.0%. Ningún fold cumplió simultáneamente ambas metas.')

else:
    st.subheader('Conclusiones y límites')
    st.markdown('''- El modelo final V3 obtuvo **recall 83.33%** y **especificidad 69.00%** en test. No cumplió ambas metas al mismo tiempo.
- La validación anidada obtuvo **recall externo medio 79.4%**, lo que cuestiona la robustez del cumplimiento.
- El análisis A/B fue **simulado y pareado**; no hubo asignación aleatoria de pacientes ni intervención clínica.
- El conjunto es pequeño y específico. No hay validación clínica externa, evaluación prospectiva ni evidencia para usar el modelo como diagnóstico.
- Se recomienda conservar V3 como experimento académico y no reajustar el umbral con datos de test para forzar métricas.''')
    st.subheader('Fuentes')
    st.markdown('''- Equipo SAGAMA. *Reporte técnico de evaluación y validación*, versión V3.
- *Proyecto_Pima_Evaluacion_V3(1).ipynb* (notebook fuente de los resultados).
- [Repositorio Equipo SAGAMA](https://github.com/roquegarciaespinoza-ops/Equipo-SAGAMA)
- [Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)''')
    st.caption('Para graficar curvas ROC y precisión-recall auténticas o activar predicciones sobre nuevos registros, se requieren los artefactos y probabilidades del notebook original. No se han inventado esos datos.')
