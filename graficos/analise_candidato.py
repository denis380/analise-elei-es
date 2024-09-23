import plotly.express as px
from dash import dcc, html

def criar_layout(df):
    # Agrupar apenas por NM_LOCAL_VOTACAO e NM_VOTAVEL, somando os votos
    df_agrupado = df.groupby(['NM_LOCAL_VOTACAO', 'NM_VOTAVEL'])['QT_VOTOS'].sum().reset_index()
    df_agrupado['NM_LOCAL_VOTACAO'] = df_agrupado['NM_LOCAL_VOTACAO'].astype(str)
    # df_agrupado = df.groupby(['NM_LOCAL_VOTACAO', 'NM_VOTAVEL']).agg({'QT_VOTOS': 'sum'})
    
    # Criar o gráfico com os dados agrupados
    fig = px.bar(df_agrupado, x='NM_LOCAL_VOTACAO', y='QT_VOTOS', color='NM_VOTAVEL',
                 barmode='group',  # Modo de barras empilhadas
                 title='Votos por escola')

    # Layout com o gráfico
    return html.Div(className="container", children=[
        html.H1("Votos por escola"), 
        dcc.Graph(id='votos-por-local', figure=fig)
    ])
