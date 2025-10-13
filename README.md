# DashBoard_Streamlit
# Dashboard proyecto / Electiva IV 
- Creacion de un dashboard que permita una comprension completa de la informacion que se necesite

- Usar streamlit para generar una ejecucion local del dashboard

- Tener en cuenta el diseño 

---

# Librerias que seran usadas para este

- Streamlit (framework web)
- Pandas (Control de datos)
- Numpy (Operaciones matematicas)
- Ploly (Diseñador grafico)

---

# Entornos para generar este proyecto
- Anaconda
- Visual Studio Code
- GitHub

---

# Comando usado para instalar las librerias 
- pip install streamlit pandas numpy plotly

---

# Configuracion inicial

## mportaciones 

- import streamlit as st
- import pandas as pd
- import numpy as np
- import plotly.express as px
- import plotly.graph_objects as go
- from datetime import datetime

## Configuracion de la pagina en el codigo
- Titulo
- Sidebard expandido
- Layout para toda la pantalla

# Ejecutar el dashboard
- streamlit run dashboard.py

# Data que sera usada para el dashboard 

- Esta sera generada de manera aleatoria por medio de codigo para que sean bastante creibles, reales a la hora de ejecutarlo

- Generacion de fechas, que empiezan desde el 2024 hasta el dia de hoy
- Generar diccionario de datos
- len (fechas) para determinar una cantidad de datos equivalente a la cantidad de dias de la data

# Diseño

 ## Declaramos el uso de html para streamlit

 - Titutlo (h1)
 - Genercion de filtros por medio de 3 selectbox para posteriormente poder organizar la infomacion segun se necesite en los graficos

- KPIs 