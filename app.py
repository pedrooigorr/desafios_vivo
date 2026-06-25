import streamlit as st
import pandas as pd

from utils.data   import carregar_dados, aplicar_filtros, criar_entrega, editar_entrega, deletar_entrega, TRANSPORTADORAS, REGIOES
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
# PONTUALIDADE + RANKING
# =====================

st.divider()

col_pont, col_rank = st.columns(2)

with col_pont:
    st.subheader("Pontualidade por Transportadora")
    st.plotly_chart(
        grafico_pontualidade(df_filtrado),
        use_container_width=True,
        config={"displayModeBar": False},
    )

with col_rank:
    st.subheader("🚨 Ranking de Atrasos")
    st.plotly_chart(
        grafico_ranking_transportadoras(df_atrasadas),
        use_container_width=True,
        config={"displayModeBar": False},
    )

# =====================
# PIZZA + MAPA
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

# =====================
# CRUD — GERENCIAR ENTREGAS
# =====================

st.divider()
st.subheader("Gerenciar Entregas")

aba_criar, aba_editar, aba_deletar = st.tabs(["Adicionar Entrega", "Editar Entrega", "Remover Entrega"])

# ── CREATE ──────────────────────────────────────────────────────────────────
with aba_criar:
    st.markdown("**Preencha os dados da nova entrega:**")

    col_a, col_b = st.columns(2)
    with col_a:
        nova_transp  = st.selectbox("Transportadora", TRANSPORTADORAS, key="criar_transp")
        novo_prazo   = st.number_input("Prazo (dias)", min_value=1, max_value=30, value=5, key="criar_prazo")
    with col_b:
        nova_regiao  = st.selectbox("Região", REGIOES, key="criar_regiao")
        novo_real    = st.number_input("Dias Reais", min_value=1, max_value=60, value=5, key="criar_real")

    if st.button("Adicionar Entrega"):
        df = criar_entrega(df, nova_transp, nova_regiao, novo_prazo, novo_real)
        st.success(f"Entrega #{df['id_entrega'].iloc[-1]} adicionada com sucesso!")
        st.rerun()

# ── UPDATE ───────────────────────────────────────────────────────────────────
with aba_editar:
    st.markdown("**Selecione a entrega que deseja editar:**")

    ids_disponiveis = sorted(df["id_entrega"].tolist())
    id_editar = st.selectbox("ID da Entrega", ids_disponiveis, key="editar_id")

    entrega_sel = df[df["id_entrega"] == id_editar].iloc[0]

    col_c, col_d = st.columns(2)
    with col_c:
        edit_transp = st.selectbox("Transportadora", TRANSPORTADORAS,
                                   index=TRANSPORTADORAS.index(entrega_sel["transportadora"])
                                   if entrega_sel["transportadora"] in TRANSPORTADORAS else 0,
                                   key="editar_transp")
        edit_prazo  = st.number_input("Prazo (dias)", min_value=1, max_value=30,
                                      value=int(entrega_sel["prazo_dias"]), key="editar_prazo")
    with col_d:
        edit_regiao = st.selectbox("Região", REGIOES,
                                   index=REGIOES.index(entrega_sel["regiao"])
                                   if entrega_sel["regiao"] in REGIOES else 0,
                                   key="editar_regiao")
        edit_real   = st.number_input("Dias Reais", min_value=1, max_value=60,
                                      value=int(entrega_sel["dias_reais"]), key="editar_real")

    if st.button("Salvar Alterações"):
        df = editar_entrega(df, id_editar, edit_transp, edit_regiao, edit_prazo, edit_real)
        st.success(f"Entrega #{id_editar} atualizada com sucesso!")
        st.rerun()

# ── DELETE ───────────────────────────────────────────────────────────────────
with aba_deletar:
    st.markdown("**Selecione a entrega que deseja remover:**")

    id_deletar = st.selectbox("ID da Entrega", sorted(df["id_entrega"].tolist()), key="deletar_id")

    entrega_del = df[df["id_entrega"] == id_deletar].iloc[0]
    st.info(
        f"Entrega **#{id_deletar}** — {entrega_del['transportadora']} | "
        f"{entrega_del['regiao']} | Prazo: {int(entrega_del['prazo_dias'])}d | "
        f"Real: {int(entrega_del['dias_reais'])}d"
    )

    if st.button("Remover Entrega", type="primary"):
        df = deletar_entrega(df, id_deletar)
        st.success(f"Entrega #{id_deletar} removida com sucesso!")
        st.rerun()