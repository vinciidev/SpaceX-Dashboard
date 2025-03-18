import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout = "wide")

space = pd.read_csv("datasets/space_missions.csv", encoding = "latin-1" )

#barra lateral
st.logo("images/spacex.jpg")
st.sidebar.title("Dashboard Inicial")



# dashboard
st.image("images/spacex.jpg", width = 700)

st.divider()
# filtrando o dataset para apenas p/ SpaceX
df_spaceX = space[space["Company"] == "SpaceX"]


# conversão para o formato inteiro
df_spaceX["Price"] = df_spaceX["Price"].fillna(0)  # substitui None/NaN por 0
df_spaceX["Price"] = pd.to_numeric(df_spaceX["Price"], errors="coerce")

rockets_prices_unique = df_spaceX[["Rocket", "Price"]].drop_duplicates()
total_rockets = len(rockets_prices_unique)
total_missions = len(df_spaceX)


rockets_prices_unique["Price"] = pd.to_numeric(rockets_prices_unique["Price"], errors="coerce")
# somar o preço de todos os foguetes
total_price = int(rockets_prices_unique["Price"].sum())

# métricas
col1, col2, col3 = st.columns(3)
col1.metric("Valor em foguetes: ", f'U$ {total_price} Milhões')
col2.metric("Número de foguetes: ", total_rockets)
col3.metric("Número de missões: ",total_missions)


st.divider()

df_relatorio = df_spaceX[['Company', 'Rocket', 'Mission', 'Location', 'Date', 'Time', 'MissionStatus']].copy()

# convertendo a coluna 'Date' para datetime
df_relatorio['Date'] = pd.to_datetime(df_relatorio['Date'], errors='coerce')

# usar o *100 para tratar como porcentagem
status_counts = df_relatorio['MissionStatus'].value_counts(normalize=True) * 100  

# definir cores
color_map = {
    'Success': 'green',
    'Failure': 'red',
    'Partial Failure': 'yellow',
    'Prelaunch Failure': 'purple'
}

# gráfico de barras empilhadas horizontalmente (status de missão)
fig_status = go.Figure()

for status, percentage in status_counts.items():
    fig_status.add_trace(go.Bar(
        name=status,
        x=[percentage],  
        y=[''],  
        orientation='h',
        marker=dict(
            color=color_map.get(status, 'gray'), 
            line=dict(width=1.5, color='black'), 
            cornerradius=10  # propriedade para arrendodar bordas
        ),  
        text=f"{percentage:.2f}%",  
        textposition='inside'
    ))

fig_status.update_layout(
    barmode='stack',  
    title="Percentual de Sucesso em Missões: ",
    xaxis=dict(title="Percentage"),
    yaxis=dict(title="", showticklabels=False),  
    showlegend=True,
    width=300, 
    height=300   
)

# gráfico de frequência de missões
df_missions_by_date = df_relatorio.groupby(df_relatorio['Date'].dt.year).size().reset_index(name='Mission Count')

fig_missions = px.line(
    df_missions_by_date, 
    x='Date', 
    y='Mission Count', 
    title="Frequência de Missões: ",
    markers=True
)

fig_missions.update_traces(line=dict(width=3), marker=dict(size=8))
fig_missions.update_layout(width=600, height=300)  # Ajuste de tamanho

# usando columns para exibir os gráficos lado a lado no Streamlit
col1, col2 = st.columns([1, 1])

with col1:
    st.plotly_chart(fig_status)

with col2:
    st.plotly_chart(fig_missions)

st.divider()



st.title("Relátorio de missões espaciais: ")

df_relatorio = df_spaceX[['Company', 'Rocket', 'Mission', 'Location', 'Date', 'Time', 'MissionStatus']]

# converter os dados p/ date
df_relatorio['Date'] = pd.to_datetime(df_relatorio['Date'], errors='coerce')

# trocar os status para português
status_map = {
    "Sucesso": "Success",
    "Falha": "Failure",
    "Falha de Lançamento": "Prelaunch Failure",
    "Falha Parcial": "Partial Failure"
}

st.subheader("Filtros")

col1, col2 = st.columns(2)  

# filtro por Status
with col1:
    status = st.selectbox("Filtrar por Status", ["Todos", "Sucesso", "Falha", "Falha de Lançamento", "Falha Parcial"])

# filtro por Local
with col2:
    local = st.selectbox("Filtrar por Local", ["Todos"] + df_relatorio['Location'].unique().tolist())

# organizando filtros de ano e foguete em uma terceira linha de colunas
col3, col4 = st.columns(2)  # Outras duas colunas lado a lado para Ano e Foguete

# filtro por Ano
with col3:
    anos = df_relatorio['Date'].dt.year.unique().tolist()
    ano_selecionado = st.selectbox("Filtrar por Ano", ["Todos"] + sorted(anos))

# filtro por Foguete
with col4:
    foguete = st.selectbox("Filtrar por Foguete", ["Todos"] + df_relatorio['Rocket'].unique().tolist())

# botão para aplicar os filtros
filtrar = st.button("Filtrar")

# aplicando os filtros quando o botão for pressionado
if filtrar:
    if status != "Todos":
        # mapeia o status selecionado para o valor correspondente no df
        df_relatorio = df_relatorio[df_relatorio['MissionStatus'] == status_map[status]]

    if local != "Todos":
        df_relatorio = df_relatorio[df_relatorio['Location'] == local]

    if ano_selecionado != "Todos":
        df_relatorio = df_relatorio[df_relatorio['Date'].dt.year == ano_selecionado]

    if foguete != "Todos":
        df_relatorio = df_relatorio[df_relatorio['Rocket'] == foguete]


    st.dataframe(df_relatorio)

