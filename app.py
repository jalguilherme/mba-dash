import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

app = dash.Dash(__name__)

# Dados fictícios de inflação (%)
df = pd.DataFrame({
    "Cidade": [
        "São Paulo", "Rio", "Fortaleza", "Salvador", "Recife", "Belém", "Manaus", "Curitiba", "Porto Alegre",
        "São Paulo", "Rio", "Fortaleza", "Salvador", "Recife", "Belém", "Manaus", "Curitiba", "Porto Alegre",
        "São Paulo", "Rio", "Fortaleza", "Salvador", "Recife", "Belém", "Manaus", "Curitiba", "Porto Alegre"
    ],
    "Trimestre": [
        "1º Tri", "1º Tri", "1º Tri", "1º Tri", "1º Tri", "1º Tri", "1º Tri", "1º Tri", "1º Tri",
        "2º Tri", "2º Tri", "2º Tri", "2º Tri", "2º Tri", "2º Tri", "2º Tri", "2º Tri", "2º Tri",
        "3º Tri", "3º Tri", "3º Tri", "3º Tri", "3º Tri", "3º Tri", "3º Tri", "3º Tri", "3º Tri"
    ],
    "Inflação": [
        1.2, 1.0, 0.9, 1.1, 1.3, 1.0, 1.4, 1.0, 0.8,  # 1º Tri
        0.8, 1.1, 1.0, 0.9, 1.2, 1.1, 1.3, 1.0, 0.9,  # 2º Tri
        1.5, 1.2, 1.1, 1.4, 1.3, 1.2, 1.6, 1.1, 1.0   # 3º Tri
    ]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Interativo - Inflação 2024"),

    html.Label("Escolha a cidade:"),
    dcc.Dropdown(
        id="dropdown-cidade",
        options=[{"label": c, "value": c} for c in df["Cidade"].unique()],
        value="São Paulo"
    ),

    dcc.Graph(id="grafico-inflacao")
])

@app.callback(
    Output("grafico-inflacao", "figure"),
    Input("dropdown-cidade", "value")
)
def atualizar_grafico(cidade_selecionada):
    df_filtrado = df[df["Cidade"] == cidade_selecionada]
    fig = px.bar(
        df_filtrado,
        x="Trimestre",
        y="Inflação",
        title=f"Inflação Trimestral - {cidade_selecionada} (2024)",
        labels={"Inflação": "Inflação (%)"}
    )
    fig.update_traces(marker_color="orange")
    return fig

if __name__ == '__main__':
    server = app.server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))