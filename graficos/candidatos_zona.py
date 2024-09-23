import plotly.express as px
import pandas as pd
from dash import dcc, html

def criar_layout(df):
    # Agrupar e contar o número de locais por candidato
    df_grouped = df.groupby('NM_VOTAVEL')['NM_LOCAL_VOTACAO'].nunique().reset_index()
    df_grouped.columns = ['NM_VOTAVEL', 'QTD_LOCALS']
    df_grouped = df_grouped.sort_values(by='QTD_LOCALS', ascending=False)  # Ordenar do maior para o menor

    # Criar o gráfico
    fig = px.bar(df_grouped, x='NM_VOTAVEL', y='QTD_LOCALS', 
                 title='Quantidade de Locais de Votação por Candidato')

    return html.Div(className="container", children=[
        html.H1("Quantidade de Locais de Votação por Candidato"),
        dcc.Graph(id='candidatos-por-local', figure=fig)
    ])
