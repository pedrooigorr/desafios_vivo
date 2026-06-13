import streamlit as st

from utils.data   import carregar_dados, aplicar_filtros
from utils.kpis   import calcular_kpis, exibir_kpis, exibir_alerta
from utils.charts import (
    grafico_transportadoras,
    grafico_regioes,
    grafico_pizza_transportadoras,
    grafico_mapa_regioes,
)

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================

st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="🚚",
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

st.sidebar.title("⚙️ Painel de Filtros")
st.sidebar.markdown("Selecione os critérios para analisar o desempenho logístico.")

regioes = st.sidebar.multiselect(
    "Selecione a Região",
    sorted(df["regiao"].unique()),
)

transportadoras = st.sidebar.multiselect(
    "Selecione a Transportadora",
    sorted(df["transportadora"].unique()),
)

df_filtrado  = aplicar_filtros(df, regioes, transportadoras)
df_atrasadas = df_filtrado[df_filtrado["atrasada"]]

# =====================
# KPIs E ALERTA
# =====================

kpis = calcular_kpis(df_filtrado, df_atrasadas)
exibir_kpis(kpis)
exibir_alerta(kpis["percentual_atraso"])

# =====================
# GRÁFICOS — TRANSPORTADORAS x REGIÕES
# =====================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚚 Comparação entre Transportadoras")
    st.plotly_chart(
        grafico_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col2:
    st.subheader("🗺️ Análise por Região")
    st.plotly_chart(
        grafico_regioes(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# =====================
# TRANSPORTADORAS MAIS PROBLEMÁTICAS + MAPA
# =====================

st.divider()
st.subheader("🚨 Transportadoras Mais Problemáticas")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        grafico_pizza_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col4:
    st.plotly_chart(
        grafico_mapa_regioes(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# =====================
# BASE DE DADOS
# =====================

st.divider()
st.subheader("📋 Base de Dados")

st.dataframe(
    df_filtrado[["id_entrega", "transportadora", "regiao", "prazo_dias", "dias_reais", "atrasada"]],
    hide_index=True,
    use_container_width=True,
)