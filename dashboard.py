#############################
#########Librerias###########
#############################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
    fechas = pd.date_range(start="2024-01-01", end=datetime.today(), freq='D')
    
    # Generar datos por categoría
    categorias = ['Camisetas', 'Pantalones', 'Sacos', 'Conjuntos']
    datos_completos = []
    
    for fecha in fechas:
        for categoria in categorias:
            datos_completos.append({
                'fecha': fecha,
                'categoria': categoria,
                'ingresos_diarios': np.random.normal(12500, 3750, 1)[0],
                'usuarios_activos': np.random.normal(3000, 750, 1)[0],
                'conversion_rate': np.random.normal(2.5, 0.8, 1)[0],
                'costo_adquisicion': np.random.normal(45, 12, 1)[0],
                'ltv_cliente': np.random.normal(180, 40, 1)[0],
                'costo_operacional': np.random.normal(5000, 1500, 1)[0]
            })
    
    df = pd.DataFrame(datos_completos)
    
    # Agregar tendencia de crecimiento
    for categoria in categorias:
        mask = df['categoria'] == categoria
        df.loc[mask, 'ingresos_diarios'] *= (1 + np.arange(mask.sum()) * 0.0001)
    
    return df

# Inicializar datos en session_state (solo se genera una vez por sesión)
if 'df_completo' not in st.session_state:
    st.session_state.df_completo = generar_datos_empresa()

# Usar los datos almacenados en session_state
df_completo = st.session_state.df_completo

######################
######TITULO##########
######################

st.markdown('<h1 class="main-header"> TeeGomix </h1>', unsafe_allow_html=True)

######################
#######FILTROS########
######################

col1, col2, col3 = st.columns(3)

with col1:
    periodo = st.selectbox("Periodo: ",
                            ["Últimos 30 días", "Último trimestre", "Último año"])

with col2:
    categoria = st.selectbox("Categoría: ",
                            ["General", "Camisetas", "Pantalones", "Sacos", "Conjuntos"])

with col3:
    comparacion = st.selectbox("Comparar con: ",
                            ["Periodo anterior", "Año pasado", "Promedio"])

############################
####Aplicar Filtros#########
############################

# Filtro de Periodo
fecha_fin = df_completo['fecha'].max()

if periodo == "Últimos 30 días":
    fecha_inicio = fecha_fin - timedelta(days=30)
    fecha_inicio_comparacion = fecha_inicio - timedelta(days=30)
    fecha_fin_comparacion = fecha_inicio
elif periodo == "Último trimestre":
    fecha_inicio = fecha_fin - timedelta(days=90)
    fecha_inicio_comparacion = fecha_inicio - timedelta(days=90)
    fecha_fin_comparacion = fecha_inicio
else:  # Último año
    fecha_inicio = fecha_fin - timedelta(days=365)
    fecha_inicio_comparacion = fecha_inicio - timedelta(days=365)
    fecha_fin_comparacion = fecha_inicio

# Filtrar por fecha
df_periodo = df_completo[df_completo['fecha'] >= fecha_inicio].copy()

# Filtro de Categoría
if categoria == "General":
    df_filtrado = df_periodo.groupby('fecha').agg({
        'ingresos_diarios': 'sum',
        'usuarios_activos': 'sum',
        'conversion_rate': 'mean',
        'costo_adquisicion': 'mean',
        'ltv_cliente': 'mean',
        'costo_operacional': 'sum'
    }).reset_index()
else:
    df_filtrado = df_periodo[df_periodo['categoria'] == categoria].copy()

# Datos para comparación
if comparacion == "Periodo anterior":
    df_comparacion = df_completo[
        (df_completo['fecha'] >= fecha_inicio_comparacion) & 
        (df_completo['fecha'] < fecha_fin_comparacion)
    ]
elif comparacion == "Año pasado":
    fecha_inicio_anio = fecha_inicio - timedelta(days=365)
    fecha_fin_anio = fecha_fin - timedelta(days=365)
    df_comparacion = df_completo[
        (df_completo['fecha'] >= fecha_inicio_anio) & 
        (df_completo['fecha'] <= fecha_fin_anio)
    ]
else:  # Promedio
    df_comparacion = df_completo[df_completo['fecha'] < fecha_inicio]

# Aplicar mismo filtro de categoría a datos de comparación
if categoria == "General":
    df_comparacion = df_comparacion.groupby('fecha').agg({
        'ingresos_diarios': 'sum',
        'usuarios_activos': 'sum',
        'conversion_rate': 'mean',
        'costo_adquisicion': 'mean',
        'ltv_cliente': 'mean',
        'costo_operacional': 'sum'
    }).reset_index()
else:
    df_comparacion = df_comparacion[df_comparacion['categoria'] == categoria].copy()

######################
#####Calcular KPIs####
######################

def calcular_cambio_porcentual(actual, anterior):
    if anterior == 0:
        return 0
    return ((actual - anterior) / anterior) * 100

# KPIs actuales
ingresos_total = df_filtrado['ingresos_diarios'].sum()
usuarios_prom = df_filtrado['usuarios_activos'].mean()
conv = df_filtrado['conversion_rate'].mean()
cac = df_filtrado['costo_adquisicion'].mean()
ltv = df_filtrado['ltv_cliente'].mean()
costos_total = df_filtrado['costo_operacional'].sum()
ganancia_neta = ingresos_total - costos_total

# KPIs de comparación
ingresos_comparacion = df_comparacion['ingresos_diarios'].sum()
usuarios_comparacion = df_comparacion['usuarios_activos'].mean()
conv_comparacion = df_comparacion['conversion_rate'].mean()
cac_comparacion = df_comparacion['costo_adquisicion'].mean()

# Calcular cambios porcentuales
cambio_ingresos = calcular_cambio_porcentual(ingresos_total, ingresos_comparacion)
cambio_usuarios = calcular_cambio_porcentual(usuarios_prom, usuarios_comparacion)
cambio_conv = calcular_cambio_porcentual(conv, conv_comparacion)
cambio_cac = calcular_cambio_porcentual(cac, cac_comparacion)

######################
#######KPIs###########
######################

st.markdown("## KPIs TeeGomix")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Ingresos Totales", f"${ingresos_total:,.0f}", f"{cambio_ingresos:.1f}%")

with col2:
    st.metric("Ganancia Neta", f"${ganancia_neta:,.0f}", 
            f"{(ganancia_neta/ingresos_total*100):.1f}% margen")

with col3:
    st.metric("Usuarios Activos", f"{usuarios_prom:.0f}", f"{cambio_usuarios:.1f}%")

with col4:
    st.metric("Tasa de Conversión", f"{conv:.2f}%", f"{cambio_conv:.2f}%")

with col5:
    ratio_ltv_cac = ltv / cac if cac > 0 else 0
    st.metric("Ratio LTV/CAC", f"{ratio_ltv_cac:.1f}x", 
            " Exitoso" if ratio_ltv_cac > 3 else " Mejorar")

################################
#########GRAFICOS###############
################################

st.markdown("## Análisis de Tendencias")
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado['fecha'], 
        y=df_filtrado['ingresos_diarios'], 
        mode='lines', 
        name='Ingresos Reales', 
        line=dict(color='#1d4e79', width=2),
        fill='tozeroy',
        fillcolor='rgba(29, 78, 121, 0.1)'
    ))
    
    # Línea de tendencia
    z = np.polyfit(range(len(df_filtrado)), df_filtrado['ingresos_diarios'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=df_filtrado['fecha'], 
        y=p(range(len(df_filtrado))), 
        mode='lines', 
        name='Tendencia', 
        line=dict(color='red', dash='dash', width=2)
    ))
    
    fig.update_layout(
        title=f"Evolución de Ingresos - {categoria}", 
        height=400, 
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Evolución de Tasa de Conversión
    fig_conv = go.Figure()
    fig_conv.add_trace(go.Scatter(
        x=df_filtrado['fecha'],
        y=df_filtrado['conversion_rate'],
        mode='lines+markers',
        name='Tasa de Conversión',
        line=dict(color='#28a745', width=2),
        marker=dict(size=4)
    ))
    
    # Línea promedio
    promedio_conv = df_filtrado['conversion_rate'].mean()
    fig_conv.add_hline(y=promedio_conv, line_dash="dash", 
                    line_color="orange", 
                    annotation_text=f"Promedio: {promedio_conv:.2f}%")
    
    fig_conv.update_layout(
        title="Evolución de Tasa de Conversión",
        height=400,
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig_conv, use_container_width=True)

############################
###Comparación Categorías###
############################

st.markdown("## Análisis por Categoría")
col1, col2 = st.columns(2)

with col1:
    # Ventas por categoría en el periodo
    df_por_categoria = df_periodo.groupby('categoria').agg({
        'ingresos_diarios': 'sum'
    }).reset_index()
    df_por_categoria = df_por_categoria.sort_values('ingresos_diarios', ascending=False)
    
    fig_categorias = px.bar(
        df_por_categoria,
        x='categoria',
        y='ingresos_diarios',
        title="Ingresos por Categoría",
        color='ingresos_diarios',
        color_continuous_scale='Blues',
        text_auto='.2s'
    )
    fig_categorias.update_traces(textposition='outside')
    fig_categorias.update_layout(
        height=400,
        template="plotly_white",
        showlegend=False,
        xaxis_title="Categoría",
        yaxis_title="Ingresos ($)"
    )
    st.plotly_chart(fig_categorias, use_container_width=True)

with col2:
    # Usuarios activos por categoría
    df_usuarios_cat = df_periodo.groupby('categoria').agg({
        'usuarios_activos': 'sum',
        'conversion_rate': 'mean'
    }).reset_index()
    
    fig_usuarios = go.Figure()
    fig_usuarios.add_trace(go.Bar(
        x=df_usuarios_cat['categoria'],
        y=df_usuarios_cat['usuarios_activos'],
        name='Usuarios Activos',
        marker_color='#6c757d',
        text=df_usuarios_cat['usuarios_activos'].round(0),
        textposition='outside'
    ))
    
    fig_usuarios.update_layout(
        title="Usuarios Activos por Categoría",
        height=400,
        template="plotly_white",
        xaxis_title="Categoría",
        yaxis_title="Usuarios"
    )
    st.plotly_chart(fig_usuarios, use_container_width=True)

############################
###Rentabilidad y Funnel####
############################

st.markdown("## Rentabilidad y Conversión")
col1, col2 = st.columns(2)

with col1:
    # Relación CAC vs LTV
    fig_rentabilidad = go.Figure()
    
    categorias_list = ['Camisetas', 'Pantalones', 'Sacos', 'Conjuntos']
    cac_por_cat = []
    ltv_por_cat = []
    
    for cat in categorias_list:
        df_cat = df_periodo[df_periodo['categoria'] == cat]
        cac_por_cat.append(df_cat['costo_adquisicion'].mean())
        ltv_por_cat.append(df_cat['ltv_cliente'].mean())
    
    fig_rentabilidad.add_trace(go.Bar(
        name='CAC (Costo)',
        x=categorias_list,
        y=cac_por_cat,
        marker_color='#dc3545'
    ))
    
    fig_rentabilidad.add_trace(go.Bar(
        name='LTV (Valor)',
        x=categorias_list,
        y=ltv_por_cat,
        marker_color='#28a745'
    ))
    
    fig_rentabilidad.update_layout(
        title="CAC vs LTV por Categoría",
        barmode='group',
        height=400,
        template="plotly_white",
        yaxis_title="Valor ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig_rentabilidad, use_container_width=True)

with col2:
    # Funnel de conversión con datos dinámicos
    usuarios_base = df_filtrado['usuarios_activos'].sum()
    tasa_conv = df_filtrado['conversion_rate'].mean() / 100
    
    visitantes = int(usuarios_base)
    leads = int(visitantes * 0.25)
    oportunidades = int(leads * 0.25)
    clientes = int(oportunidades * tasa_conv * 10)
    
    etapas = ['Visitantes', 'Leads', 'Oportunidades', 'Clientes']
    valores = [visitantes, leads, oportunidades, clientes]
    
    funnel = go.Figure(go.Funnel(
        y=etapas, 
        x=valores, 
        textinfo="value+percent initial",
        marker=dict(color=['#3b5998', '#8b9dc3', '#dfe3ee', '#f7f7f7'])
    ))
    funnel.update_layout(
        title="Funnel de Conversión", 
        height=400, 
        template="plotly_white"
    )
    st.plotly_chart(funnel, use_container_width=True)

############################
#########Ana_Geogra#########
############################

st.markdown("## Análisis Geográfico")

# Generar datos geográficos consistentes usando session_state
if 'datos_geograficos' not in st.session_state:
    paises = ['México', 'Colombia', 'Chile', 'Argentina', 'Perú', 'España']
    st.session_state.datos_geograficos = {
        'paises': paises,
        'ventas': np.random.uniform(10000, 100000, len(paises))
    }

df_geo = pd.DataFrame({
    'País': st.session_state.datos_geograficos['paises'],
    'Ventas': st.session_state.datos_geograficos['ventas']
})

mapa = px.bar(
    df_geo,
    x='País', 
    y='Ventas', 
    color='Ventas', 
    color_continuous_scale='Viridis', 
    title="Ventas por Región",
    text_auto='.2s'
)
mapa.update_traces(textposition='outside')
mapa.update_layout(height=400, template="plotly_white", showlegend=False)
st.plotly_chart(mapa, use_container_width=True)

############################
#####Top 5 Mejores Días#####
############################

st.markdown("## Top 5 Mejores Días de Ventas")

df_top_dias = df_filtrado.nlargest(5, 'ingresos_diarios')[['fecha', 'ingresos_diarios']].copy()
df_top_dias['fecha'] = df_top_dias['fecha'].dt.strftime('%d/%m/%Y')
df_top_dias.columns = ['Fecha', 'Ingresos']
df_top_dias['Ingresos'] = df_top_dias['Ingresos'].apply(lambda x: f"${x:,.0f}")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.dataframe(df_top_dias, hide_index=True, use_container_width=True)

with col2:
    st.metric("Mejor Día", df_top_dias.iloc[0]['Fecha'])
    
with col3:
    st.metric("Ingresos Máximos", df_top_dias.iloc[0]['Ingresos'])

#############################
#######Alert_Intel###########
#############################

st.markdown("## Centro de Alertas Inteligentes")
alertas = []

# Comparar últimos 7 días con los 7 anteriores
if len(df_filtrado) >= 14:
    ingresos_recientes = df_filtrado.tail(7)['ingresos_diarios'].mean()
    ingresos_anteriores = df_filtrado.iloc[-14:-7]['ingresos_diarios'].mean()
    
    if ingresos_recientes < ingresos_anteriores:
        alertas.append({
            'tipo': 'Advertencia', 
            'mensaje': 'Ingresos por debajo del promedio en los últimos 7 días', 
            'color': 'orange'
        })

if df_filtrado['conversion_rate'].tail(1).iloc[0] < 2.0:
    alertas.append({
        'tipo': 'Crítico', 
        'mensaje': 'Tasa de conversión < 2%. Acción inmediata requerida', 
        'color': 'red'
    })

if df_filtrado['usuarios_activos'].tail(1).iloc[0] > df_filtrado['usuarios_activos'].quantile(0.9):
    alertas.append({
        'tipo': 'Éxito', 
        'mensaje': 'Usuarios activos en top 10% histórico', 
        'color': 'green'
    })

# Alerta de rentabilidad
if ratio_ltv_cac < 3:
    alertas.append({
        'tipo': 'Advertencia',
        'mensaje': f'Ratio LTV/CAC bajo ({ratio_ltv_cac:.1f}x). Objetivo: >3x',
        'color': 'orange'
    })

if not alertas:
    st.info(" No hay alertas en este momento. Todo funciona correctamente.")
else:
    for alerta in alertas:
        st.markdown(f"""
        <div style="padding: 1rem; margin: 0.5rem 0; background-color: {alerta['color']};
                    color: white; border-radius: 10px; font-weight:bold;">
            {alerta['tipo']}: {alerta['mensaje']}
        </div>
        """, unsafe_allow_html=True)

############################
#######Insights Auto########
############################

st.markdown("##  Insights Automáticos")

col1, col2, col3 = st.columns(3)

with col1:
    mejor_categoria = df_por_categoria.iloc[0]
    st.info(f" **Categoría Líder:** {mejor_categoria['categoria']} genera ${mejor_categoria['ingresos_diarios']:,.0f} en ingresos")

with col2:
    tendencia = "crecimiento" if cambio_ingresos > 0 else "decrecimiento"
    st.info(f" **Tendencia:** Tus ingresos están en {tendencia} del {abs(cambio_ingresos):.1f}%")

with col3:
    if ratio_ltv_cac > 3:
        st.success(f" **Rentabilidad Excelente:** Por cada $1 invertido, recuperas ${ratio_ltv_cac:.1f}")
    else:
        st.warning(f" **Mejorar CAC:** Ratio LTV/CAC actual: {ratio_ltv_cac:.1f}x (meta: >3x)")

############################
#####Info de Filtros########
############################

st.markdown("---")
st.caption(f" Mostrando datos de: **{categoria}** | Periodo: **{periodo}** | Comparando con: **{comparacion}**")