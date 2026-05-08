from __future__ import annotations

from typing import Any

import pandas as pd


def head(data: list[dict[str, Any]], n: int = 5) -> list[dict[str, Any]]:
    return data[:n]


def clean_health_data(raw_data: list[dict]) -> pd.DataFrame:
    """Pipeline básica de limpieza para datos de salud.

    - Convierte la lista de dicts a DataFrame.
    - Elimina filas completamente vacías.
    - Elimina duplicados.
    - Normaliza nombres de columnas (lower, strip, espacios -> '_').
    - Convierte columnas numéricas que vienen como texto.
    """
    if raw_data is None:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    if df.empty:
        return df

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    df.columns = [
        str(col).strip().lower().replace(" ", "_") for col in df.columns
    ]

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        try:
            converted = pd.to_numeric(df[col])
            df[col] = converted
        except (ValueError, TypeError):
            continue

    df = df.reset_index(drop=True)
    return df
