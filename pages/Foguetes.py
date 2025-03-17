import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout = "wide")

space = pd.read_csv("datasets/space_missions.csv", encoding = "latin-1" )

st.logo("images/spacex.jpg")

#Titulo da barra lateral
st.sidebar.title("Dashboard SpaceX")
st.sidebar.markdown("Escolha um foguete! E veja quais foram suas missões espaciais 🚀")


# Sidebar para selecionar o foguete (já filtrado pela empresa)
rockets = space.loc[space["Company"] == 'SpaceX', "Rocket"].unique()
ship = st.sidebar.selectbox("Foguetes", rockets)


# Status da nave
shipStatus = space.loc[space["Rocket"] == ship, "RocketStatus"].unique()
status_map = {"Active": "Ativo", "Retired": "Inativo"}
shipStatus = [status_map.get(status, status) for status in shipStatus]  # Substitui apenas se houver correspondência

shipPrice = space.loc[space["Rocket"] == ship, "Price"].unique()

st.title(ship)
st.subheader(f"Situação: {', '.join(shipStatus)}")


st.divider()

# Filtrar as linhas que correspondem ao foguete selecionado
missions_info = space.loc[space["Rocket"] == ship, ["Mission", "Location", "Date", "Time", "MissionStatus"]]

# Exibir as missões e as informações adicionais
st.subheader("Missões desse foguete:")

if not missions_info.empty:
    for index, row in missions_info.iterrows():
        st.write(f"**Missão:** {row['Mission']}")
        st.write(f"**Localização:** {row['Location']}")
        st.write(f"**Data:** {row['Date']}")
        st.write(f"**Hora:** {row['Time']}")
        st.write(f"**Status da Missão:** {row['MissionStatus']}")
        st.write("---")  # Linha de separação entre as missões
else:
    st.write("Nenhuma missão encontrada para este foguete.")