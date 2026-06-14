import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Paleta centralizada ──────────────────────────────────────────────────────
AZUL_ESCURO  = "#1E3A5F"
AZUL_MEDIO   = "#2E5C99"
AZUL_CLARO1  = "#4A80C4"
AZUL_CLARO2  = "#7AAEDD"
AZUL_CLARO3  = "#B8D4F0"
TEXTO        = "#111827"
GRADE        = "#E5E7EB"
VERDE        = "#059669"
VERMELHO     = "#DC2626"

_PALETA_PIE  = [AZUL_ESCURO, AZUL_MEDIO, AZUL_CLARO1, AZUL_CLARO2, AZUL_CLARO3]
_PALETA_MAPA = [AZUL_CLARO3, AZUL_MEDIO, AZUL_ESCURO]

TODAS_REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

REGIOES_COORDS = {
    "Norte":        {"lat": -4.0,  "lon": -62.0, "sigla": "NO"},
    "Nordeste":     {"lat": -9.0,  "lon": -40.0, "sigla": "NE"},
    "Centro-Oeste": {"lat": -15.0, "lon": -53.0, "sigla": "CO"},
    "Sudeste":      {"lat": -20.0, "lon": -44.0, "sigla": "SE"},
    "Sul":          {"lat": -27.0, "lon": -52.0, "sigla": "SL"},
}


def _layout_base(title: str, height: int = None, margin: dict = None) -> dict:
    base = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=20, color=AZUL_ESCURO),
        margin=margin or dict(l=40, r=40, t=60, b=40),
    )
    if height:
        base["height"] = height
    return base


def grafico_transportadoras(df_atrasadas: pd.DataFrame) -> go.Figure:
    """Barras horizontal — atrasos por transportadora."""
    if df_atrasadas.empty:
        fig = go.Figure()
        fig.update_layout(
            **_layout_base("", margin=dict(l=40, r=60, t=60, b=40)),
            title_text="Quantidade de Entregas Atrasadas por Transportadora",
            annotations=[dict(
                text="Nenhum atraso registrado para os filtros selecionados.",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=15, color=TEXTO)
            )]
        )
        return fig

    dados = (
        df_atrasadas
        .groupby("transportadora")
        .size()
        .reset_index(name="atrasos")
        .sort_values("atrasos", ascending=True)
    )

    fig = px.bar(
        dados, x="atrasos", y="transportadora", orientation="h",
        title="Quantidade de Entregas Atrasadas por Transportadora",
        color_discrete_sequence=[AZUL_ESCURO],
    )

    fig.update_layout(
        **_layout_base("", margin=dict(l=40, r=60, t=60, b=40)),
        showlegend=False,
        xaxis=dict(
            title=dict(text="Quantidade de Atrasos", font=dict(size=16, color=TEXTO), standoff=15),
            tickfont=dict(size=14, color=TEXTO), gridcolor=GRADE,
        ),
        yaxis=dict(
            title=dict(text="Transportadora", font=dict(size=16, color=TEXTO), standoff=15),
            tickfont=dict(size=14, color=TEXTO),
        ),
    )

    fig.update_traces(
        marker_line_width=1.5, marker_line_color="#0F172A",
        textposition="outside", texttemplate="%{x}",
        textfont=dict(size=16, color=TEXTO, weight="bold"), width=0.5,
    )

    return fig


def grafico_regioes(df_atrasadas: pd.DataFrame) -> go.Figure:
    """Barras vertical — atrasos por região (todas, mesmo zeradas)."""
    contagem = (
        df_atrasadas.groupby("regiao").size().reset_index(name="atrasos")
    )
    base  = pd.DataFrame({"regiao": TODAS_REGIOES})
    dados = base.merge(contagem, on="regiao", how="left").fillna(0)
    dados["atrasos"] = dados["atrasos"].astype(int)
    dados = dados.sort_values("atrasos", ascending=False)

    fig = px.bar(
        dados, x="regiao", y="atrasos",
        title="Entregas Atrasadas por Região",
        color_discrete_sequence=[AZUL_ESCURO],
    )

    fig.update_layout(
        **_layout_base(""),
        xaxis=dict(
            title=dict(text="Região", font=dict(size=16, color=TEXTO), standoff=15),
            tickfont=dict(size=14, color=TEXTO),
        ),
        yaxis=dict(
            title=dict(text="Quantidade de Atrasos", font=dict(size=16, color=TEXTO), standoff=15),
            tickfont=dict(size=14, color=TEXTO), gridcolor=GRADE,
        ),
    )

    fig.update_traces(
        marker_line_width=1.5, marker_line_color="#0F172A",
        textposition="outside", texttemplate="%{y}",
        textfont=dict(size=16, color=TEXTO, weight="bold"), width=0.35,
    )

    return fig


def grafico_pizza_transportadoras(df_atrasadas: pd.DataFrame) -> go.Figure:
    """Pizza — dias totais de atraso por transportadora."""
    if df_atrasadas.empty:
        fig = go.Figure()
        fig.update_layout(
            **_layout_base("", height=420),
            title_text="Proporção de Dias de Atraso",
            annotations=[dict(
                text="Nenhum atraso registrado para os filtros selecionados.",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=15, color=TEXTO)
            )]
        )
        return fig

    dados = (
        df_atrasadas
        .groupby("transportadora")
        .agg(dias_totais_atraso=("dias_atraso", "sum"))
        .reset_index()
        .sort_values("dias_totais_atraso", ascending=False)
    )

    fig = px.pie(
        dados, names="transportadora", values="dias_totais_atraso",
        title="Proporção de Dias de Atraso",
        color_discrete_sequence=_PALETA_PIE,
    )

    fig.update_layout(
        **_layout_base("", height=420, margin=dict(l=20, r=140, t=60, b=20)),
        legend=dict(
            font=dict(size=13, color=TEXTO), orientation="v",
            x=1.02, y=0.5, xanchor="left", yanchor="middle",
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_traces(
        textposition="inside", textinfo="percent+label",
        textfont=dict(size=13, color="white"),
        marker=dict(line=dict(color="#FFFFFF", width=2)),
    )

    return fig


def grafico_ranking_transportadoras(df_atrasadas: pd.DataFrame) -> go.Figure:
    """Ranking numerado — dias totais de atraso por transportadora."""
    if df_atrasadas.empty:
        fig = go.Figure()
        fig.update_layout(
            **_layout_base("", height=420),
            title_text="Ranking — Dias Totais de Atraso",
            annotations=[dict(
                text="Nenhum atraso registrado para os filtros selecionados.",
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=15, color=TEXTO)
            )]
        )
        return fig

    dados = (
        df_atrasadas
        .groupby("transportadora")
        .agg(atrasos=("atrasada", "count"), dias_atraso=("dias_atraso", "sum"))
        .reset_index()
        .sort_values("dias_atraso", ascending=False)
        .reset_index(drop=True)
    )
    dados["label"] = [f"#{i+1} {t}" for i, t in enumerate(dados["transportadora"].tolist())]

    fig = px.bar(
        dados, x="dias_atraso", y="label", orientation="h",
        title="🏆 Ranking — Dias Totais de Atraso",
        color="dias_atraso",
        color_continuous_scale=[AZUL_CLARO2, AZUL_ESCURO],
        text="dias_atraso",
    )

    fig.update_layout(
        **_layout_base("", height=420, margin=dict(l=20, r=60, t=60, b=40)),
        showlegend=False, coloraxis_showscale=False,
        xaxis=dict(
            title=dict(text="Dias Totais de Atraso", font=dict(size=14, color=TEXTO), standoff=10),
            tickfont=dict(size=13, color=TEXTO), gridcolor=GRADE,
        ),
        yaxis=dict(
            title=dict(text="", font=dict(size=14, color=TEXTO)),
            tickfont=dict(size=14, color=TEXTO, weight="bold"),
            autorange="reversed",
        ),
    )

    fig.update_traces(
        textposition="outside", texttemplate="%{x} dias",
        textfont=dict(size=14, color=TEXTO, weight="bold"),
        marker_line_width=1.5, marker_line_color="#0F172A", width=0.5,
    )

    return fig


def grafico_pontualidade(df_filtrado: pd.DataFrame) -> go.Figure:
    """Barras empilhadas — pontualidade vs atraso por transportadora."""
    dados = (
        df_filtrado
        .groupby(["transportadora", "atrasada"])
        .size()
        .reset_index(name="quantidade")
    )
    dados["status"] = dados["atrasada"].map({True: "Atrasada", False: "No Prazo"})

    fig = px.bar(
        dados, x="transportadora", y="quantidade", color="status",
        title="Pontualidade por Transportadora",
        color_discrete_map={"Atrasada": VERMELHO, "No Prazo": VERDE},
        barmode="stack", text="quantidade",
    )

    fig.update_layout(
        **_layout_base(""),
        legend=dict(
            title="", font=dict(size=13, color=TEXTO),
            orientation="h", x=0.5, y=1.08,
            xanchor="center", bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            title=dict(text="Transportadora", font=dict(size=14, color=TEXTO), standoff=10),
            tickfont=dict(size=13, color=TEXTO),
        ),
        yaxis=dict(
            title=dict(text="Quantidade de Entregas", font=dict(size=14, color=TEXTO), standoff=10),
            tickfont=dict(size=13, color=TEXTO), gridcolor=GRADE,
        ),
    )

    fig.update_traces(
        textfont=dict(size=13, color="white", weight="bold"),
        textposition="inside",
        marker_line_width=1, marker_line_color="#FFFFFF",
        width=0.35,
    )

    return fig


def grafico_mapa_regioes(df_atrasadas: pd.DataFrame) -> go.Figure:
    """Mapa de bolhas — atrasos por região do Brasil."""
    atrasos = (
        df_atrasadas.groupby("regiao").agg(atrasos=("atrasada", "count")).reset_index()
    )

    base   = pd.DataFrame({"regiao": list(REGIOES_COORDS.keys())})
    atrasos = base.merge(atrasos, on="regiao", how="left").fillna(0)
    atrasos["atrasos"]  = atrasos["atrasos"].astype(int)
    atrasos["lat"]      = atrasos["regiao"].map(lambda r: REGIOES_COORDS[r]["lat"])
    atrasos["lon"]      = atrasos["regiao"].map(lambda r: REGIOES_COORDS[r]["lon"])
    atrasos["sigla"]    = atrasos["regiao"].map(lambda r: REGIOES_COORDS[r]["sigla"])
    atrasos["tamanho"]  = atrasos["atrasos"].apply(lambda x: max(x * 6, 4))

    fig = px.scatter_geo(
        atrasos, lat="lat", lon="lon", size="tamanho", color="atrasos",
        hover_name="regiao",
        hover_data={"atrasos": True, "lat": False, "lon": False, "tamanho": False, "sigla": False},
        text="sigla", title="Mapa de Atrasos por Região do Brasil",
        color_continuous_scale=_PALETA_MAPA, size_max=22, scope="south america",
    )

    fig.update_geos(
        visible=True, resolution=50,
        showcountries=True, countrycolor="#9CA3AF",
        showcoastlines=True, coastlinecolor="#9CA3AF",
        showland=True, landcolor="#F3F4F6",
        showocean=True, oceancolor="#DBEAFE",
        showlakes=False, showsubunits=True, subunitcolor="#D1D5DB",
        center={"lat": -16.0, "lon": -52.0}, projection_scale=2.2,
    )

    fig.update_traces(
        textfont=dict(size=13, color=AZUL_ESCURO, weight="bold"),
        textposition="top center",
        marker=dict(line=dict(color="#FFFFFF", width=1.5)),
    )

    fig.update_layout(
        **_layout_base("", height=420, margin=dict(l=0, r=0, t=60, b=0)),
        coloraxis_colorbar=dict(
            title=dict(text="Atrasos", font=dict(size=13, color=TEXTO)),
            tickfont=dict(size=12, color=TEXTO), thickness=14, len=0.6,
        ),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
    )

    return fig