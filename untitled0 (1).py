
from datetime import date
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import streamlit as st

#streamlit run codigoBase.py

# Lendo o dataset
try:
    df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
except Exception as e:
    print("Erro ao carregar o dataset:", e)
    exit()

# Garantindo que a coluna 'date' seja do tipo datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Melhorando o nome das colunas da tabela
df = df.rename(columns={
    'newDeaths': 'Novos óbitos',
    'newCases': 'Novos casos',
    'deaths_per_100k_inhabitants': 'Obitos por 100 mil habitantes',
    'totalCases_per_100k_inhabitants': 'Casos por 100 mil habitantes'
})

# Seleção do estado
estados = list(df['state'].unique())
state = st.sidebar.selectbox('Qual estado?', estados)



# Verificando se o estado selecionado existe no dataset
if state not in estados:
    print(f"Estado '{state}' não encontrado no dataset. Estados disponíveis: {', '.join(estados)}")
    exit()

# Seleção da coluna
#column = 'Casos por 100 mil habitantes'
colunas = ['Novos óbitos', 'Novos casos', 'Obitos por 100 mil habitantes', 'Casos por 100 mil habitantes']
columns = st.sidebar.selectbox('Qual tipo de informação?', colunas)

# Verificando se a coluna selecionada existe no dataset
if column not in colunas:
    print(f"Coluna '{column}' não encontrada. Colunas disponíveis: {', '.join(colunas)}")
    exit()

# Seleção das linhas que pertencem ao estado
df_state = df[df['state'] == state]

# Criando o gráfico
fig = px.line(df_state, x='date', y=column, title=f'{column} - {state}')
fig.update_layout(xaxis_title='Data', yaxis_title=column.upper(), title={'x': 0.5})

# Mensagem ao usuário
st.title('DADOS COVID - BRASIL')
st.write('Nessa aplicação, o usuário tem a opção de escolher o estado e o tipo de informação para mostrar o gráfico. Utilize o menu lateral para análise.')

# Exibindo o gráfico
st.plotly_chart(fig, use_container__width=True)

!pip uninstall ipywidgets jupyterlab_widgets -y
