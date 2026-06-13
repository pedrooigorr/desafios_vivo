import pandas as pd
import streamlit as st


def calcular_kpis(df_filtrado: pd.DataFrame, df_atrasadas: pd.DataFrame) -> dict:
    """Calcula os indicadores principais e retorna em dicionário."""
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

    return {
        "total_entregas":      total_entregas,
        "entregas_atrasadas":  entregas_atrasadas,
        "percentual_atraso":   percentual_atraso,
        "pior_transportadora": pior_transportadora,
    }


def exibir_kpis(kpis: dict) -> None:
    """Renderiza os 4 cards de KPI na interface."""
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total de Entregas",      kpis["total_entregas"])
    col2.metric("Entregas Atrasadas",     kpis["entregas_atrasadas"])
    col3.metric("% de Atraso",            f"{kpis['percentual_atraso']:.1f}%")
    col4.metric("Transportadora Crítica", kpis["pior_transportadora"])


def exibir_alerta(percentual_atraso: float) -> None:
    """Exibe alerta visual de acordo com o nível de atraso."""
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