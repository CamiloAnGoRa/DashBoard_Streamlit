#############################
#########Librerias###########
#############################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

#############################
#######Configuraciones#######
#############################

st.set_page_config(
    page_title = "Dashboard Electiva IV",
    layout ="wide",
    initial_sidebar_state ="expanded"

)

############################
######Generar_Data##########
############################

def generar_datos_empresa():
    fechas = pd.date_range(start="2024-01-01", end=datetime.today(),freq='D')
    datos = {
        'fecha': fechas,
        'ingresos_diarios': np.random.normal(50000, 15000, len(fechas)),
        'usuarios_activos': np.random.normal(12000, 3000, len(fechas)),
        'conversion_rate': np.random.normal(2.5, 0.8, len(fechas)),
        'costo_adquisicion': np.random.normal(45, 12, len(fechas)),
        'ltv_cliente': np.random.normal(180, 40, len(fechas))
    }

    df = pd.DataFrame(datos)
    df['ingresos_diarios'] *= (1+ np.arange(len(df)) * 0.0001) #Tendencia de crecimiento constante 

    return df

df = generar_datos_empresa() #Llamar a la funcion para generar los datos


######################
######TITULO##########
######################

st.markdown('<h1 class="main-header"> TeeGomix </h1>',
            unsafe_allow_html=True
            )


######################
#######FILTROS########
######################

col1, col2, col3 = st.columns(3)
with col1:
    periodo = st.selectbox ("Periodo: ",
                            ["Últimos 30 días", "Último trimestre", "Último año"])
with col2:
    categoria = st.selectbox("Categoría: ",
                            ["General", "Ventas", "Marketing", "Producto"])
with col3:
    comparacion = st.selectbox("Comparar con: ",
                            ["Periodo anterior", "Año pasado", "Promedio"])


######################
#######KPIs###########
######################

st.markdown("KPIs TeeGomix")
col1, col2, col3, col4 = st.columns(4)

with col1:
    ingresos_total = df['ingresos_diarios'].sum()
    st.metric("Ingresos Totales", f"${ingresos_total:,.0f}", f"{np.random.uniform(5, 15):.1f}%")

with col2:
    usuarios_prom = df['usuarios_activos'].mean()
    st.metric("Usuarios Activos", f"{usuarios_prom:.0f}", f"{np.random.uniform(2, 8):.1f}%")

with col3:
    conv = df['conversion_rate'].mean()
    st.metric("Tasa de Conversion", f"{conv:.2f}", f"{np.random.uniform(-0.5, 1.2):.2f}%")

with col4:
    cac = df['costo_adquisicion'].mean()
    st.metric("CAC Promedio", f"${cac:.0f}", f"-{np.random.uniform(2, 8):.1f}%")