import pandas as pd
import streamlit as st


def calcular_kpis(df_filtrado: pd.DataFrame, df_atrasadas: pd.DataFrame) -> dict:
    total_entregas     = len(df_filtrado)
    entregas_atrasadas = len(df_atrasadas)

    percentual_atraso = (
        entregas_atrasadas / total_entregas * 100
        if total_entregas > 0 else 0
    )

    pior_transportadora = (
        df_atrasadas["transportadora"].value_counts().idxmax()
        if len(df_atrasadas) > 0 else "-"
    )

    media_dias_atraso = (
        round(df_atrasadas["dias_atraso"].mean(), 1)
        if len(df_atrasadas) > 0 else 0
    )

    return {
        "total_entregas":      total_entregas,
        "entregas_atrasadas":  entregas_atrasadas,
        "percentual_atraso":   percentual_atraso,
        "pior_transportadora": pior_transportadora,
        "media_dias_atraso":   media_dias_atraso,
    }


def exibir_kpis(kpis: dict) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total de Entregas",       kpis["total_entregas"])
    col2.metric("Entregas Atrasadas",      kpis["entregas_atrasadas"])
    col3.metric("% de Atraso",             f"{kpis['percentual_atraso']:.1f}%")
    col4.metric("Transportadora Crítica",  kpis["pior_transportadora"])
    col5.metric("Média de Dias de Atraso", f"{kpis['media_dias_atraso']} dias")


def exibir_alerta(percentual_atraso: float) -> None:
    if percentual_atraso >= 50:
        st.error(f"🚨 Situação crítica: {percentual_atraso:.1f}% das entregas estão atrasadas.")
    elif percentual_atraso >= 30:
        st.warning(f"⚠️ Atenção: {percentual_atraso:.1f}% das entregas estão atrasadas.")
    else:
        st.success(f"✅ Operação controlada: apenas {percentual_atraso:.1f}% das entregas estão atrasadas.")


def gerar_insight(df_atrasadas: pd.DataFrame, percentual_atraso: float) -> str:
    if len(df_atrasadas) == 0:
        return "✅ Nenhuma entrega atrasada encontrada para os filtros selecionados."

    ranking = (
        df_atrasadas
        .groupby("transportadora")
        .agg(dias=("dias_atraso", "sum"), qtd=("atrasada", "count"))
        .sort_values("dias", ascending=False)
    )
    pior_transp  = ranking.index[0]
    pior_dias    = int(ranking.iloc[0]["dias"])
    pior_qtd     = int(ranking.iloc[0]["qtd"])
    total_dias   = int(ranking["dias"].sum())
    pior_pct     = round(pior_dias / total_dias * 100, 1) if total_dias > 0 else 0
    pior_regiao  = df_atrasadas["regiao"].value_counts().idxmax()
    pior_reg_qtd = int(df_atrasadas["regiao"].value_counts().iloc[0])

    return (
        f"📌 **{pior_transp}** lidera com **{pior_dias} dias** acumulados de atraso "
        f"em {pior_qtd} entrega(s) — representando **{pior_pct}%** do total de dias perdidos. "
        f"A região mais crítica é **{pior_regiao}**, com {pior_reg_qtd} entrega(s) atrasada(s). "
        f"Recomenda-se revisão imediata do contrato com {pior_transp} e reforço operacional no {pior_regiao}."
    )