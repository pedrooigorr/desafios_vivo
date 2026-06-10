import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================

st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="📦",
    layout="wide"
)



st.markdown("""
<style>

/* Fundo principal */
.stApp {
    background-color: #F5F5F5;
}

/* Título principal */
h1 {
    color: #1E3A5F;
}

/* Subtítulos */
h2, h3 {
    color: #1E3A5F;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# =====================
# CABEÇALHO
# =====================

st.title("📦 Dashboard Logístico Inteligente")

st.caption(
    "Monitoramento de atrasos logísticos e desempenho operacional em tempo real"
)

# =====================
# CARREGAMENTO DOS DADOS
# =====================

df = pd.read_csv("dados.csv")

# =====================
# COLUNAS CALCULADAS
# =====================

df["atrasada"] = df["dias_reais"] > df["prazo_dias"]

df["dias_atraso"] = (
    df["dias_reais"] - df["prazo_dias"]
)

# =====================
# FILTROS
# =====================

st.sidebar.title("⚙️ Painel de Filtros")

st.sidebar.markdown(
    "Selecione os critérios para analisar o desempenho logístico."
)

regioes = st.sidebar.multiselect(
    "Selecione a Região",
    sorted(df["regiao"].unique())
)

transportadoras = st.sidebar.multiselect(
    "Selecione a Transportadora",
    sorted(df["transportadora"].unique())
)

# =====================
# APLICAÇÃO DOS FILTROS
# =====================

df_filtrado = df.copy()

if regioes:
    df_filtrado = df_filtrado[
        df_filtrado["regiao"].isin(regioes)
    ]

if transportadoras:
    df_filtrado = df_filtrado[
        df_filtrado["transportadora"].isin(transportadoras)
    ]

# =====================
# DADOS DE ATRASO
# =====================

df_atrasadas = df_filtrado[
    df_filtrado["atrasada"]
]

# =====================
# KPIs
# =====================

total_entregas = len(df_filtrado)

entregas_atrasadas = len(df_atrasadas)

percentual_atraso = (
    entregas_atrasadas / total_entregas * 100
) if total_entregas > 0 else 0

if len(df_atrasadas) > 0:
    pior_transportadora = (
        df_atrasadas["transportadora"]
        .value_counts()
        .idxmax()
    )
else:
    pior_transportadora = "-"

# =====================
# INDICADORES
# =====================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de Entregas",
    total_entregas
)

col2.metric(
    "Entregas Atrasadas",
    entregas_atrasadas
)

col3.metric(
    "% de Atraso",
    f"{percentual_atraso:.1f}%"
)

col4.metric(
    "Transportadora Crítica",
    pior_transportadora
)

# =====================
# ALERTA VISUAL
# =====================

if percentual_atraso >= 50:
    st.error(
        f"🚨 Situação crítica: {percentual_atraso:.1f}% das entregas estão atrasadas."
    )

elif percentual_atraso >= 30:
    st.warning(
        f"⚠️ Atenção: {percentual_atraso:.1f}% das entregas estão atrasadas."
    )

else:
    st.success(
        f"✅ Operação controlada: apenas {percentual_atraso:.1f}% das entregas estão atrasadas."
    )

# =====================
# COMPARAÇÃO ENTRE TRANSPORTADORAS
# =====================

ranking_transportadoras = (
    df_atrasadas
    .groupby("transportadora")
    .size()
    .reset_index(name="atrasos")
    .sort_values(
        "atrasos",
        ascending=False
    )
)

fig_transportadoras = px.bar(
    ranking_transportadoras,
    x="transportadora",
    y="atrasos",
    title="Quantidade de Entregas Atrasadas por Transportadora",
    color_discrete_sequence=["#1E3A5F"]
)

fig_transportadoras.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    

    title_font_size=0,

    xaxis_title="Transportadora",
    yaxis_title="Quantidade de Atrasos",

    font=dict(
        size=12,
        color="#1E3A5F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

fig_transportadoras.update_traces(
    marker_line_width=2,
    marker_line_color="#0F172A",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=18,
        color="black"
    ),
    width=0.4
)

fig_transportadoras.update_traces(
    width=0.6
)

# =====================
# ANÁLISE POR REGIÃO
# =====================

ranking_regioes = (
    df_atrasadas
    .groupby("regiao")
    .size()
    .reset_index(name="atrasos")
    .sort_values(
        "atrasos",
        ascending=False
    )
)

fig_regioes = px.bar(
    ranking_regioes,
    x="regiao",
    y="atrasos",
    title="Entregas Atrasadas por Região",
    color_discrete_sequence=["#F97316"]
)

fig_regioes.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",

    title_font_size=20,

    xaxis_title="Região",
    yaxis_title="Quantidade de Atrasos",

    font=dict(
        size=14,
        color="#1E3A5F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

fig_regioes.update_traces(
    marker_line_width=2,
    marker_line_color="#7C2D12",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=18,
        color="black"
    ),
    width=0.4
)

fig_regioes.update_traces(
    width=0.6
)

fig_regioes.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# =====================
# GRÁFICOS LADO A LADO
# =====================

st.divider()

col_graf1, col_graf2 = st.columns([1, 1])

with col_graf1:

    st.subheader(
        "🚚 Comparação entre Transportadoras"
    )

    st.plotly_chart(
    fig_transportadoras,
    use_container_width=True,
    config={"displayModeBar": False}
)

with col_graf2:

    st.subheader(
        "🗺️ Análise por Região"
    )

    st.plotly_chart(
    fig_regioes,
    use_container_width=True,
    config={"displayModeBar": False}
)

# =====================
# RANKING DE PROBLEMAS
# =====================

st.divider()

st.subheader(
    "🚨 Ranking das Transportadoras Mais Problemáticas"
)

ranking_problemas = (
    df_atrasadas
    .groupby("transportadora")
    .agg(
        quantidade_atrasos=("atrasada", "count"),
        dias_totais_atraso=("dias_atraso", "sum")
    )
    .reset_index()
    .sort_values(
        "dias_totais_atraso",
        ascending=False
    )
)

fig_problemas = px.bar(
    ranking_problemas,
    x="transportadora",
    y="dias_totais_atraso",
    color="dias_totais_atraso",
    color_continuous_scale=[
        "#FDE68A",
        "#F59E0B",
        "#EF4444",
        "#991B1B"
    ],
    title="Dias Totais de Atraso por Transportadora"
)

fig_problemas.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",

    title_font_size=22,

    xaxis_title="Transportadora",
    yaxis_title="Dias Totais de Atraso",

    font=dict(
        size=14,
        color="#1E3A5F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

fig_problemas.update_traces(
    marker_line_width=2,
    marker_line_color="black",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=18,
        color="black"
    ),
    width=0.4
)

fig_problemas.update_traces(
    width=0.6
)

fig_problemas.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig_problemas,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.dataframe(
    ranking_problemas,
    hide_index=True,
    use_container_width=True
)

# =====================
# BASE DE DADOS
# =====================

st.divider()

st.subheader("📋 Base de Dados")

st.dataframe(
    df_filtrado[
        [
            "id_entrega",
            "transportadora",
            "regiao",
            "prazo_dias",
            "dias_reais",
            "dias_atraso",
            "atrasada"
        ]
    ],
    hide_index=True,
    use_container_width=True
)