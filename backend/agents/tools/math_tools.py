from __future__ import annotations

import numpy as np
import pandas as pd


def safe_div(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b


def detect_anomalies(
    df: pd.DataFrame,
    value_col: str,
    threshold: float = 2.0,
) -> list[dict]:
    """Detecta filas anómalas según la regla mean + threshold * std.

    Devuelve las filas cuyo valor en `value_col` supera ese umbral, como
    lista de diccionarios. Si la columna no existe o no es numérica, retorna [].
    """
    try:
        if df is None or df.empty or value_col not in df.columns:
            return []

        series = pd.to_numeric(df[value_col], errors="coerce")
        if series.dropna().empty:
            return []

        mean = float(series.mean())
        std = float(series.std(ddof=0))
        if np.isnan(std) or std == 0:
            return []

        upper_bound = mean + threshold * std
        mask = series > upper_bound
        anomalies = df.loc[mask].copy()
        return anomalies.to_dict(orient="records")
    except (ValueError, TypeError, KeyError):
        return []


def calculate_trend_summary(df: pd.DataFrame, value_col: str) -> dict:
    """Calcula estadísticas básicas (suma, promedio, max, min) sobre `value_col`."""
    try:
        if df is None or df.empty or value_col not in df.columns:
            return {"total": 0.0, "promedio": 0.0, "max": 0.0, "min": 0.0, "n": 0}

        series = pd.to_numeric(df[value_col], errors="coerce").dropna()
        if series.empty:
            return {"total": 0.0, "promedio": 0.0, "max": 0.0, "min": 0.0, "n": 0}

        return {
            "total": float(series.sum()),
            "promedio": float(series.mean()),
            "max": float(series.max()),
            "min": float(series.min()),
            "n": int(series.count()),
        }
    except (ValueError, TypeError, KeyError):
        return {"total": 0.0, "promedio": 0.0, "max": 0.0, "min": 0.0, "n": 0}


def analyze_ips_by_department(df: pd.DataFrame) -> tuple[dict, list[dict]]:
    """Analiza IPS contando registros por departamento y detecta concentraciones atípicas."""
    if df is None or df.empty or "depa_nombre" not in df.columns:
        return {}, []

    counts = df["depa_nombre"].value_counts()
    if counts.empty:
        return {}, []

    mean = float(counts.mean())
    std = float(counts.std(ddof=0))
    threshold = mean + 2.0 * std if std > 0 else mean

    summary = {
        "total_registros": int(len(df)),
        "departamentos_distintos": int(counts.shape[0]),
        "promedio_ips_por_departamento": round(mean, 2),
        "max_ips_en_un_departamento": int(counts.max()),
        "departamento_con_mas_ips": str(counts.idxmax()),
        "n": int(len(df)),
    }

    anomalies = [
        {"depa_nombre": str(dept), "conteo_ips": int(count)}
        for dept, count in counts.items()
        if count > threshold
    ]
    return summary, anomalies
