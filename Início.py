import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout = "wide")

space = pd.read_csv("datasets/space_missions.csv", encoding = "latin-1" )

st.logo("images/spacex.jpg")
#Titulo da barra lateral
st.sidebar.title("Dashboard Inicial")
st.sidebar.markdown("- Métricas gerais ")
st.sidebar.markdown("- Análise de missões espaciais ")


st.image("images/spacex.jpg", width = 700)

st.divider()
# Filtrando o dataset para a empresa SpaceX
df_spaceX = space[space["Company"] == "SpaceX"]


# Conversão para o formato inteiro
df_spaceX["Price"] = df_spaceX["Price"].fillna(0)  # Substitui None/NaN por 0
df_spaceX["Price"] = pd.to_numeric(df_spaceX["Price"], errors="coerce")

rockets_prices_unique = df_spaceX[["Rocket", "Price"]].drop_duplicates()
total_rockets = len(rockets_prices_unique)
total_missions = len(df_spaceX)


rockets_prices_unique["Price"] = pd.to_numeric(rockets_prices_unique["Price"], errors="coerce")
# Somar o preço de todos os foguetes
total_price = int(rockets_prices_unique["Price"].sum())

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Valor em foguetes: ", f'U$ {total_price} Milhões')
col2.metric("Número de foguetes: ", total_rockets)
col3.metric("Número de missões: ",total_missions)



st.divider()


st.title("Relátorio de missões espaciais")
df_relatorio = df_spaceX[['Company', 'Rocket', 'Mission', 'Location', 'Date', 'Time', 'MissionStatus']]
df_relatorio










