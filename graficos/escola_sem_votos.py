from dash import dcc, html

def criar_layout(df):
    return html.Div(className="container", 
                    style={'padding-top': '30px', 'padding-bottom': '30px'},
                    children=[
        html.H1("Escolas onde o candidato não teve votos"),
        
        html.Div(
            className="row", 
            children=[
            html.Div(
                className="col-md-6", 
                style={'display' : 'grid', 'place-items' : 'center'},
                
                children=[
                html.H1(id='total-escolas-sem-votos', style={'text-align' : 'center'})
            ]),
            
            # Coluna 2: Lista de escolas sem votos
            html.Div(className="col-md-6", 
                style={
                    "height": "300px",
                    "overflow-y": "auto",
                    "border": "1px solid #ccc;",
                    "padding": 0,
                    "margin": 0,
                    "list-style-type": "none",
                },
                children=[
          
                html.Ul(id='lista-escolas-sem-votos')  # Lista de escolas (dinâmica)
            ])
        ])
    ])
