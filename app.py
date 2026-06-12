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

# =====================
# PAINEL DE ESTILOS (CSS CORRIGIDO)
# =====================

st.markdown("""
<style>

/* Fundo principal - cinza médio como na imagem de referência */
.stApp {
    background-color: #D1D5DB;
}

/* Header do Streamlit - fundo escuro fixo para os ícones ficarem visíveis */
header[data-testid="stHeader"] {
    background-color: #1E3A5F !important;
}

/* Ícones e botões do header brancos */
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] a,
header[data-testid="stHeader"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* Texto geral - Ajustado para nunca interferir nos eixos e textos dos gráficos Plotly */
body,
p,
label,
.stApp span:not([class*="g"]):not([class*="text"]),
.stApp div:not([class*="plotly"]):not([data-embedding="plotly"]):not([class*="js-plotly"]) {
    color: #111827 !important;
}

/* Título principal */
h1 {
    color: #1E3A5F !important;
}

/* Subtítulos */
h2, h3 {
    color: #1E3A5F !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1E3A5F;
}

/* Título e textos da sidebar */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: white !important;
}

/* Card branco para KPIs */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    border: 1px solid #E5E7EB;
}

/* Card branco para gráficos Plotly */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    border: 1px solid #E5E7EB;
}

/* Card branco para a tabela/dataframe */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    border: 1px solid #E5E7EB;
    overflow: hidden;
}

/* Força fundo branco dentro do dataframe (iframe interno) */
[data-testid="stDataFrame"] iframe {
    background-color: #FFFFFF !important;
    border-radius: 12px;
}

/* Área do conteúdo principal com leve padding para respirar */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: transparent;
}

/* Caixa principal do filtro (quando fechada) */
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #29497A !important;
    color: white !important;
    border: 2px solid #4A6FA5 !important;
    border-radius: 10px !important;
}

/* Texto de placeholder / seleção da caixa fechada */
.stMultiSelect div[data-baseweb="select"] {
    color: white !important;
}

/* Campo interno de digitação */
.stMultiSelect input {
    color: white !important;
}

/* Placeholder */
.stMultiSelect input::placeholder {
    color: #CBD5E1 !important;
}

/* Itens selecionados (Tags) */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #F97316 !important;
    border-radius: 6px !important;
}

/* Texto dos itens selecionados */
.stMultiSelect [data-baseweb="tag"] span {
    color: white !important;
}

/* =======================================================
   CORREÇÃO DA LISTA SUSPENSA (MENU ABERTO)
   ======================================================= */

/* Container geral da lista suspensa */
div[data-baseweb="popover"] ul,
div[role="listbox"] {
    background-color: #1E293B !important;
    border-radius: 10px !important;
}

/* Força TODOS os textos das opções a ficarem BRANCOS */
div[data-baseweb="popover"] li,
div[role="option"],
div[role="option"] span,
div[role="option"] div {
    color: #FFFFFF !important;
}

/* Corrige o botão "Select all" (Selecionar todos) */
div[data-baseweb="popover"] button {
    color: #FFFFFF !important;
}

/* Efeito de hover ao passar o mouse pelas opções */
div[data-baseweb="popover"] li:hover,
div[role="option"]:hover {
    background-color: #334155 !important;
}

/* KPIs */
[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 700;
}

/* Caption */
[data-testid="stCaptionContainer"] {
    color: #4B5563 !important;
}

/* =======================================================
   CORREÇÃO DO BOTÃO DE OCULTAR/MOSTRAR FILTROS (SIDEBAR)
   ======================================================= */

/* Força o botão a ficar visível com fundo azul escuro e sem transparências */
button[data-testid="stSidebarCollapseButton"] {
    background-color: #1E3A5F !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    transition: background-color 0.2s ease, transform 0.2s ease !important;
}

/* Garante que os ícones das setinhas de dentro do botão fiquem brancos */
button[data-testid="stSidebarCollapseButton"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Efeito ao passar o mouse no botão da sidebar (muda para um tom mais escuro) */
button[data-testid="stSidebarCollapseButton"]:hover {
    background-color: #111827 !important;
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

df = pd.DataFrame({
    "id_entrega": [301, 302, 303, 304, 305, 306, 307, 308, 309, 310],
    "transportadora": ["RotaMax", "ViaCargo", "FlashLog", "RotaMax", "ViaCargo",
                       "FlashLog", "RotaMax", "ViaCargo", "FlashLog", "ViaCargo"],
    "regiao": ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste",
               "Sul", "Sul", "Sudeste", "Norte", "Nordeste"],
    "prazo_dias": [3, 5, 4, 6, 2, 5, 6, 3, 5, 4],
    "dias_reais": [7, 5, 9, 4, 6, 12, 9, 4, 5, 8]
})

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
    .sort_values("atrasos", ascending=False)
)

fig_transportadoras = px.bar(
    ranking_transportadoras,
    x="transportadora",
    y="atrasos",
    title="Quantidade de Entregas Atrasadas por Transportadora",
    color_discrete_sequence=["#1E3A5F"]
)

fig_transportadoras.update_layout(
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=20, color="#1E3A5F"),
    margin=dict(l=40, r=40, t=60, b=40),
    xaxis=dict(
        title=dict(
            text="Transportadora",
            font=dict(size=16, color="#111827"),
            standoff=15                            # Correção: standoff movido para dentro de title
        ),
        tickfont=dict(size=14, color="#111827")
    ),
    yaxis=dict(
        title=dict(
            text="Quantidade de Atrasos",
            font=dict(size=16, color="#111827"),
            standoff=15                            # Correção: standoff movido para dentro de title
        ),
        tickfont=dict(size=14, color="#111827"),
        gridcolor="#E5E7EB"
    )
)

fig_transportadoras.update_traces(
    marker_line_width=1.5,
    marker_line_color="#0F172A",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=16,
        color="#111827",
        weight="bold"
    ),
    width=0.35
)

# =====================
# ANÁLISE POR REGIÃO
# =====================

ranking_regioes = (
    df_atrasadas
    .groupby("regiao")
    .size()
    .reset_index(name="atrasos")
    .sort_values("atrasos", ascending=False)
)

fig_regioes = px.bar(
    ranking_regioes,
    x="regiao",
    y="atrasos",
    title="Entregas Atrasadas por Região",
    color_discrete_sequence=["#F97316"]
)

fig_regioes.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=20, color="#1E3A5F"),
    margin=dict(l=40, r=40, t=60, b=40),
    xaxis=dict(
        title=dict(
            text="Região",
            font=dict(size=16, color="#111827"),
            standoff=15
        ),
        tickfont=dict(size=14, color="#111827")
    ),
    yaxis=dict(
        title=dict(
            text="Quantidade de Atrasos",
            font=dict(size=16, color="#111827"),
            standoff=15
        ),
        tickfont=dict(size=14, color="#111827"),
        gridcolor="#E5E7EB"
    )
)

fig_regioes.update_traces(
    marker_line_width=1.5,
    marker_line_color="#7C2D12",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=16,
        color="#111827",
        weight="bold"
    ),
    width=0.35
)

# =====================
# GRÁFICOS LADO A LADO
# =====================

st.divider()

col_graf1, col_graf2 = st.columns([1, 1])

with col_graf1:
    st.subheader("🚚 Comparação entre Transportadoras")
    st.plotly_chart(
        fig_transportadoras,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col_graf2:
    st.subheader("🗺️ Análise por Região")
    st.plotly_chart(
        fig_regioes,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =====================
# RANKING DE PROBLEMAS
# =====================

st.divider()

st.subheader("🚨 Ranking das Transportadoras Mais Problemáticas")

ranking_problemas = (
    df_atrasadas
    .groupby("transportadora")
    .agg(
        quantidade_atrasos=("atrasada", "count"),
        dias_totais_atraso=("dias_atraso", "sum")
    )
    .reset_index()
    .sort_values("dias_totais_atraso", ascending=False)
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
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=22, color="#1E3A5F"),
    margin=dict(l=40, r=40, t=60, b=40),
    
    xaxis=dict(
        title=dict(
            text="Transportadora",
            font=dict(size=16, color="#111827"),
            standoff=15
        ),
        tickfont=dict(size=14, color="#111827")
    ),
    
    yaxis=dict(
        title=dict(
            text="Dias Totais de Atraso",
            font=dict(size=16, color="#111827"),
            standoff=15
        ),
        tickfont=dict(size=14, color="#111827"),
        gridcolor="#E5E7EB"
    ),
    
    coloraxis_colorbar=dict(
        title=dict(
            text="Dias Totais",
            font=dict(size=14, color="#111827")
        ),
        tickfont=dict(size=12, color="#111827")
    )
)

fig_problemas.update_traces(
    marker_line_width=1.5,
    marker_line_color="black",
    textposition="outside",
    texttemplate="%{y}",
    textfont=dict(
        size=16,
        color="#111827",
        weight="bold"
    ),
    width=0.35
)

st.plotly_chart(
    fig_problemas,
    use_container_width=True,
    config={"displayModeBar": False}
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