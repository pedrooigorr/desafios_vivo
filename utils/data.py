import pandas as pd
import os


def carregar_dados() -> pd.DataFrame:
    """
    Carrega os dados do arquivo dados.csv se existir,
    caso contrário usa os dados de exemplo embutidos.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "..", "dados.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame({
            "id_entrega":     [301, 302, 303, 304, 305, 306, 307, 308, 309, 310],
            "transportadora": ["RotaMax", "ViaCargo", "FlashLog", "RotaMax", "ViaCargo",
                               "FlashLog", "RotaMax", "ViaCargo", "FlashLog", "ViaCargo"],
            "regiao":         ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste",
                               "Sul", "Sul", "Sudeste", "Norte", "Nordeste"],
            "prazo_dias":     [3, 5, 4, 6, 2, 5, 6, 3, 5, 4],
            "dias_reais":     [7, 5, 9, 4, 6, 12, 9, 4, 5, 8],
        })

    return processar_dados(df)


def processar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas calculadas ao DataFrame."""
    df["atrasada"]   = df["dias_reais"] > df["prazo_dias"]
    df["dias_atraso"] = df["dias_reais"] - df["prazo_dias"]
    return df


def aplicar_filtros(
    df: pd.DataFrame,
    regioes: list,
    transportadoras: list,
) -> pd.DataFrame:
    """Aplica filtros de região e transportadora ao DataFrame."""
    df_filtrado = df.copy()

    if regioes:
        df_filtrado = df_filtrado[df_filtrado["regiao"].isin(regioes)]

    if transportadoras:
        df_filtrado = df_filtrado[df_filtrado["transportadora"].isin(transportadoras)]

    return df_filtrado