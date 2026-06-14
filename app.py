import streamlit as st
import pandas as pd

from utils.data   import carregar_dados, aplicar_filtros
from utils.kpis   import calcular_kpis, exibir_kpis, exibir_alerta, gerar_insight
from utils.charts import (
    grafico_transportadoras,
    grafico_regioes,
    grafico_pizza_transportadoras,
    grafico_ranking_transportadoras,
    grafico_pontualidade,
    grafico_mapa_regioes,
)

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================

st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="",
    layout="wide",
)

# =====================
# CSS EXTERNO
# =====================

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =====================
# CABEÇALHO
# =====================

st.title("Dashboard Logístico Inteligente")
st.caption("Monitoramento de atrasos logísticos e desempenho operacional em tempo real")

# =====================
# DADOS
# =====================

df = carregar_dados()

# =====================
# FILTROS (SIDEBAR)
# =====================

st.sidebar.title("Painel de Filtros")
st.sidebar.markdown("Selecione os critérios para analisar o desempenho logístico.")

# Inicializa session_state para os filtros
if "regioes" not in st.session_state:
    st.session_state["regioes"] = []
if "transportadoras" not in st.session_state:
    st.session_state["transportadoras"] = []

# Botão de limpar filtros — reseta antes de renderizar os multiselects
if st.sidebar.button("Limpar Filtros"):
    st.session_state["regioes"] = []
    st.session_state["transportadoras"] = []

regioes = st.sidebar.multiselect(
    "Selecione a Região",
    sorted(df["regiao"].unique()),
    default=st.session_state["regioes"],
    key="regioes",
)

transportadoras = st.sidebar.multiselect(
    "Selecione a Transportadora",
    sorted(df["transportadora"].unique()),
    default=st.session_state["transportadoras"],
    key="transportadoras",
)

df_filtrado  = aplicar_filtros(df, regioes, transportadoras)
df_atrasadas = df_filtrado[df_filtrado["atrasada"]]

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"Exibindo **{len(df_filtrado)}** de **{len(df)}** entregas"
)
st.sidebar.markdown(
    f"**{len(df_atrasadas)}** entrega(s) atrasada(s)"
)

# =====================
# KPIs E ALERTA
# =====================

kpis = calcular_kpis(df_filtrado, df_atrasadas)
exibir_kpis(kpis)
exibir_alerta(kpis["percentual_atraso"])

# =====================
# INSIGHT AUTOMÁTICO
# =====================

st.info(gerar_insight(df_atrasadas, kpis["percentual_atraso"]))

# =====================
# GRAFICOS — TRANSPORTADORAS x REGIOES
# =====================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Comparação entre Transportadoras")
    st.plotly_chart(
        grafico_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col2:
    st.subheader("Análise por Região")
    st.plotly_chart(
        grafico_regioes(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# =====================
# PONTUALIDADE
# =====================

st.divider()
st.subheader("Pontualidade por Transportadora")
st.plotly_chart(
    grafico_pontualidade(df_filtrado),
    use_container_width=True,
    config={"displayModeBar": False},
)

# =====================
# RANKING + PIZZA + MAPA
# =====================

st.divider()
st.subheader("Transportadoras Mais Problemáticas")

col3, col4, col5 = st.columns(3)

with col3:
    st.plotly_chart(
        grafico_ranking_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col4:
    st.plotly_chart(
        grafico_pizza_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col5:
    st.plotly_chart(
        grafico_mapa_regioes(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# =====================
# BASE DE DADOS COM DESTAQUE
# =====================

st.divider()
st.subheader("Base de Dados")

csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Exportar CSV",
    data=csv,
    file_name="entregas_filtradas.csv",
    mime="text/csv",
)

def colorir_linhas(row):
    if row["atrasada"] == "❌ Sim":
        return ["background-color: #FEE2E2; color: #991B1B"] * len(row)
    return ["background-color: #F0FDF4; color: #166534"] * len(row)

df_exibir = df_filtrado[[
    "id_entrega", "transportadora", "regiao",
    "prazo_dias", "dias_reais", "atrasada"
]].copy()

df_exibir["atrasada"] = df_exibir["atrasada"].map({True: "❌ Sim", False: "✅ Não"})

st.dataframe(
    df_exibir.style.apply(colorir_linhas, axis=1),
    hide_index=True,
    use_container_width=True,
)