from dash import dcc, html

def get():
    return html.Nav(className="navbar navbar-expand-lg navbar-light bg-light", children=[
            html.Link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'),
            html.A("Home", href="/", className="navbar-brand"),
            html.Div(className="collapse navbar-collapse", children=[
                html.Ul(className="navbar-nav mr-auto", children=[
                    html.Li(className="nav-item", children=[
                        html.A("Análise por escolas", href="/analise_escolas", className="nav-link")
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A("Análise de Candidatos", href="/analise_candidato", className="nav-link")
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A("Tabela", href="/tabela", className="nav-link")
                    ])
                ])
            ])
        ])