import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Simulação de um dataset de vendas

np.random.seed(42)
paises = ["Brazil", "Argentina", "Chile", "Colombia", "Mexico", "Peru"]
anos = list(range(2015, 2024))
categorias = ["Eletrônicos", "Roupas", "Alimentos", "Brinquedos"]

df_vendas = pd.DataFrame({
    "País": np.random.choice(paises, 200),
    "Ano": np.random.choice(anos, 200),
    "Categoria": np.random.choice(categorias, 200),
    "Vendas": np.random.randint(1000, 50000, 200),
    "Lucro": np.random.randint(200, 20000, 200)
})

# Mapeamento fictício 
map_iso = {
    "Brazil": "BRA",
    "Argentina": "ARG",
    "Chile": "CHL",
    "Colombia": "COL",
    "Mexico": "MEX",
    "Peru": "PER"
}
df_vendas["ISO"] = df_vendas["País"].map(map_iso)

# Layout Streamlit
st.set_page_config(layout="wide", page_title="Dashboard de Vendas – América Latina")
st.title("📊 Dashboard de Vendas – América Latina")

st.sidebar.header("Filtros")
ano_sel = st.sidebar.slider(
    "Ano",
    min_value=min(anos),
    max_value=max(anos),
    value=max(anos),
    step=1
)

categorias_sel = st.sidebar.multiselect(
    "Categoria",
    categorias,
    default=categorias
)
paises_sel = st.sidebar.multiselect(
    "País",
    paises,
    default=paises
)

df_filtro = df_vendas[
    (df_vendas["Ano"] == ano_sel) &
    (df_vendas["Categoria"].isin(categorias_sel)) &
    (df_vendas["País"].isin(paises_sel))
]

col1, col2 = st.columns(2)

# Gráfico 1 - Dispersão Vendas vs Lucro 
with col1:
    st.subheader("💰 Vendas x Lucro por País")
    if df_filtro.empty:
        st.info("Nenhum dado para os filtros selecionados.")
    else:
        fig_disp = px.scatter(
            df_filtro,
            x="Vendas",
            y="Lucro",
            size="Vendas",
            color="Categoria",
            hover_name="País",
            text="País",  
            size_max=60,
            labels={"Vendas": "Total de Vendas (R$)", "Lucro": "Lucro (R$)"},
            title=f"Dispersão Vendas/Lucro – {ano_sel}"
        )

        margem_x = max(1, int(df_filtro["Vendas"].max() * 0.1))
        margem_y = max(1, int(df_filtro["Lucro"].max() * 0.1))
        fig_disp.update_xaxes(range=[0, df_filtro["Vendas"].max() + margem_x])
        fig_disp.update_yaxes(range=[0, df_filtro["Lucro"].max() + margem_y])

        fig_disp.update_traces(
            mode="markers+text",
            textposition="top center",
            textfont=dict(size=10)
        )

        st.plotly_chart(fig_disp, use_container_width=True)

# Gráfico 2 - Mapa de Vendas 
with col2:
    st.subheader("🗺️ Vendas por País (América Latina)")
    if df_filtro.empty:
        st.info("Nenhum dado para os filtros selecionados.")
    else:
        df_map = df_filtro.groupby(["País", "ISO"], as_index=False)["Vendas"].sum()
        fig_mapa = px.choropleth(
            df_map,
            locations="ISO",
            color="Vendas",
            hover_name="País",
            color_continuous_scale="Blues",
            labels={"Vendas": "Vendas Totais (R$)"},
            title=f"Distribuição Geográfica das Vendas – {ano_sel}",
            projection="mercator"
        )
        
        fig_mapa.update_geos(
            showcountries=True,
            showcoastlines=True,
            showland=True,
            lataxis_range=[-56, 33],
            lonaxis_range=[-120, -30],
            resolution=50
        )
        st.plotly_chart(fig_mapa, use_container_width=True)

# Tabela de dados filtrados
st.markdown("### 📋 Tabela de Dados Filtrados")
st.dataframe(df_filtro.reset_index(drop=True))