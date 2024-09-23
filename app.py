from flask import Flask, render_template
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.dash_table import DataTable
import plotly.express as px
import pandas as pd
from graficos import candidato_votos_zona, escola_sem_votos
from templates.components import navbar

# Criar o servidor Flask
server = Flask(__name__)

# Carregar o CSV
caminho_do_arquivo = 'votacao_secao_2020_MG/votos_contagem_vereadores.csv'
try:
    dados = pd.read_csv(caminho_do_arquivo, encoding='utf-8', delimiter=',')
except:
    try:
        dados = pd.read_csv(caminho_do_arquivo, encoding='ISO-8859-1', delimiter=',')
    except:
        dados = pd.read_csv(caminho_do_arquivo, encoding='cp1252', delimiter=',')

df = pd.DataFrame(dados)
df['ANO_ELEICAO'] = df['ANO_ELEICAO'].astype(int)
df['NR_ZONA'] = df['NR_ZONA'].astype(int)
df['NR_SECAO'] = df['NR_SECAO'].astype(int)
df['NR_VOTAVEL'] = df['NR_VOTAVEL'].astype(int)
df['QT_VOTOS'] = df['QT_VOTOS'].astype(int)

# Criar a aplicação Dash para o dashboard principal
app_dash = Dash(__name__, server=server, url_base_pathname='/dash/')

# Criar a aplicação Dash para a análise de candidatos
app_analise_candidato = Dash(__name__, server=server, url_base_pathname='/analise_candidato/')

# Criar a aplicação Dash para a tabela
app_tabela = Dash(__name__, server=server, url_base_pathname='/tabela/')

# Configurar layouts para os dashboards
layout_votos_por_local = candidato_votos_zona.criar_layout(df)
layout_escola_sem_votos = escola_sem_votos.criar_layout(df)

# Definir o layout do dashboard principal
app_dash.layout = html.Div(children=[
    navbar.get(),
    html.Div([
        dcc.Dropdown(
            id='global-candidato-dropdown',
            options=[{'label': candidato, 'value': candidato} for candidato in df['NM_VOTAVEL'].unique()],
            value=df['NM_VOTAVEL'].unique()[0],  # Valor inicial
            multi=False,
            clearable=False,
            style={'width': '50%'}
        )
    ], style={'margin': '20px'}),
    
    html.Div(children=[
        layout_votos_por_local
    ]),
    
    html.Div([
        layout_escola_sem_votos  
    ])
])

# Criar o layout para o dashboard de análise de candidatos
app_analise_candidato.layout = html.Div(children=[
    navbar.get(),
    html.H1("Análise de Candidato"), 
    html.Div(children=[
        layout_votos_por_local  # Reutilizando o layout do gráfico de locais por candidato
    ])
])

# Criar o layout para a tabela
colunas_exibidas = ['ANO_ELEICAO', 'NR_ZONA', 'NR_SECAO', 'NR_VOTAVEL', 'NM_VOTAVEL', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO']  # Altere para as colunas que você quer
app_tabela.layout = html.Div(children=[
    navbar.get(),
    html.H1("Tabela de Dados"),
    DataTable(
        id='data-table',
        columns=[
            {"name": 'ANO', "id": 'ANO_ELEICAO', "type": 'numeric'}, 
            {"name": 'NÚMERO ZONA', "id": 'NR_ZONA', "type": 'numeric'}, 
            {"name": 'NÚMERO SEÇÃO', "id": 'NR_SECAO', "type": 'numeric'},
            {"name": 'NÚMERO CANDIDATO', "id": 'NR_VOTAVEL', "type": 'numeric'},
            {"name": 'CANDITATO', "id": 'NM_VOTAVEL', "type": 'text'},
            {"name": 'QTD VOTOS', "id": 'QT_VOTOS', "type": 'numeric'},
            {"name": 'LOCAL', "id": 'NM_LOCAL_VOTACAO', "type": 'text'},
            {"name": 'ENDEREÇO DO LOCAL', "id": 'DS_LOCAL_VOTACAO_ENDERECO', "type": 'text'}
        ], 
        data=df.to_dict('records'),  # Carrega os dados do CSV
        page_size=10,  # Exibe 10 linhas por página
        filter_action="native",  # Habilita a funcionalidade de filtro
        sort_action="native", 
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'minWidth': '100px', 'width': '100px', 'maxWidth': '200px',
            'whiteSpace': 'normal'
        }
    )
])

# Rota para a página principal do Flask com o DataTable
@server.route('/')
def index():
    return render_template('index.html')

# Rota para o dashboard principal
@server.route('/analise_escolas')
def render_dashboard():
    return app_dash.index()

# Rota para o novo dashboard "Análise de Candidato"
@server.route('/analise_candidato')
def render_analise_candidato():
    return app_analise_candidato.index()

# Rota para a tabela
@server.route('/tabela')
def render_tabela():
    return app_tabela.index()


@app_dash.callback(
    [Output('votos-por-local', 'figure'),  # Gráfico de candidato_votos_zona
     Output('total-escolas-sem-votos', 'children'),  # Total de escolas sem votos
     Output('lista-escolas-sem-votos', 'children')],  # Lista de escolas sem votos
    [Input('global-candidato-dropdown', 'value')]
)
def atualizar_graficos(candidato_selecionado):
    # Atualizar o gráfico de candidato_votos_zona
    df_filtrado = df[df['NM_VOTAVEL'] == candidato_selecionado]
    df_agrupado = df_filtrado.groupby(['NM_LOCAL_VOTACAO', 'NM_VOTAVEL'])['QT_VOTOS'].sum().reset_index()
    df_agrupado['NM_LOCAL_VOTACAO'] = df_agrupado['NM_LOCAL_VOTACAO'].astype(str)
    fig_votos_por_local = px.bar(df_agrupado, x='NM_LOCAL_VOTACAO', y='QT_VOTOS', color='NM_VOTAVEL',
                                 barmode='group', title=f'Votos por Local para {candidato_selecionado}')

    # Atualizar as escolas sem votos
    todas_escolas = df['NM_LOCAL_VOTACAO'].unique()
    escolas_com_votos = df_filtrado['NM_LOCAL_VOTACAO'].unique()
    escolas_sem_votos = list(set(todas_escolas) - set(escolas_com_votos))

    # Calcular o número total de escolas sem votos
    total_escolas_sem_votos = len(escolas_sem_votos)
    
    # Gerar a lista de escolas sem votos
    lista_escolas_sem_votos = [html.Li(escola) for escola in escolas_sem_votos]

    return fig_votos_por_local, total_escolas_sem_votos, lista_escolas_sem_votos


# Iniciar o servidor Flask
if __name__ == '__main__':
    server.run(debug=True)
