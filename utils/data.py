import pandas as pd
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "dados.csv")

TRANSPORTADORAS = ["FlashLog", "RotaMax", "ViaCargo"]
REGIOES         = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

DADOS_EXEMPLO = {
    "id_entrega":     [301, 302, 303, 304, 305, 306, 307, 308, 309, 310],
    "transportadora": ["RotaMax", "ViaCargo", "FlashLog", "RotaMax", "ViaCargo",
                       "FlashLog", "RotaMax", "ViaCargo", "FlashLog", "ViaCargo"],
    "regiao":         ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste",
                       "Sul", "Sul", "Sudeste", "Norte", "Nordeste"],
    "prazo_dias":     [3, 5, 4, 6, 2, 5, 6, 3, 5, 4],
    "dias_reais":     [7, 5, 9, 4, 6, 12, 9, 4, 5, 8],
}


def carregar_dados() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(DADOS_EXEMPLO)
        salvar_dados(df)

    return processar_dados(df)


def salvar_dados(df: pd.DataFrame) -> None:
    """Salva o DataFrame no CSV (sem colunas calculadas)."""
    colunas = ["id_entrega", "transportadora", "regiao", "prazo_dias", "dias_reais"]
    df[colunas].to_csv(CSV_PATH, index=False)


def processar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df["atrasada"]    = df["dias_reais"] > df["prazo_dias"]
    df["dias_atraso"] = df["dias_reais"] - df["prazo_dias"]
    return df


def aplicar_filtros(df: pd.DataFrame, regioes: list, transportadoras: list) -> pd.DataFrame:
    df_filtrado = df.copy()
    if regioes:
        df_filtrado = df_filtrado[df_filtrado["regiao"].isin(regioes)]
    if transportadoras:
        df_filtrado = df_filtrado[df_filtrado["transportadora"].isin(transportadoras)]
    return df_filtrado


def proximo_id(df: pd.DataFrame) -> int:
    return int(df["id_entrega"].max()) + 1 if len(df) > 0 else 301


def criar_entrega(df: pd.DataFrame, transportadora: str, regiao: str,
                  prazo_dias: int, dias_reais: int) -> pd.DataFrame:
    nova = pd.DataFrame([{
        "id_entrega":    proximo_id(df),
        "transportadora": transportadora,
        "regiao":         regiao,
        "prazo_dias":     prazo_dias,
        "dias_reais":     dias_reais,
    }])
    df_novo = pd.concat([df[["id_entrega", "transportadora", "regiao", "prazo_dias", "dias_reais"]], nova],
                        ignore_index=True)
    salvar_dados(df_novo)
    return processar_dados(df_novo)


def editar_entrega(df: pd.DataFrame, id_entrega: int, transportadora: str,
                   regiao: str, prazo_dias: int, dias_reais: int) -> pd.DataFrame:
    df_base = df[["id_entrega", "transportadora", "regiao", "prazo_dias", "dias_reais"]].copy()
    idx = df_base[df_base["id_entrega"] == id_entrega].index
    df_base.loc[idx, "transportadora"] = transportadora
    df_base.loc[idx, "regiao"]         = regiao
    df_base.loc[idx, "prazo_dias"]     = prazo_dias
    df_base.loc[idx, "dias_reais"]     = dias_reais
    salvar_dados(df_base)
    return processar_dados(df_base)


def deletar_entrega(df: pd.DataFrame, id_entrega: int) -> pd.DataFrame:
    df_base = df[["id_entrega", "transportadora", "regiao", "prazo_dias", "dias_reais"]].copy()
    df_base = df_base[df_base["id_entrega"] != id_entrega].reset_index(drop=True)
    salvar_dados(df_base)
    return processar_dados(df_base)