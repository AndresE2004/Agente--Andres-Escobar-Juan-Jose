from __future__ import annotations

import pandas as pd

from backend.agents.state import AgentState
from backend.agents.tools.math_tools import (
    calculate_trend_summary,
    detect_anomalies,
)
from backend.core.config import settings
from backend.core.storage import save_analysis_data


DATASET_VALUE_COLUMNS: dict[str, str] = {
    "afiliados": "numpersonas",
    "sivigila": "conteo",
}


def analista_node(state: AgentState) -> AgentState:
    df = state.get("data")

    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        print("[Agente Analista] Advertencia: no hay DataFrame válido para analizar.")
        return state

    print("📈 [Agente Analista] Iniciando análisis estadístico...")

    analysis_results: dict = {
        "dataset_type": "unknown",
        "summary": {},
        "anomalies": [],
    }

    try:
        for dataset_type, value_col in DATASET_VALUE_COLUMNS.items():
            if value_col in df.columns:
                analysis_results["dataset_type"] = dataset_type
                analysis_results["summary"] = calculate_trend_summary(df, value_col)
                analysis_results["anomalies"] = detect_anomalies(df, value_col)
                break
    except Exception as exc:
        print(f"[Agente Analista] Error durante el análisis: {exc}")
        return {**state, "analysis": analysis_results}

    n_anomalies = len(analysis_results["anomalies"])
    dtype = analysis_results["dataset_type"]
    summary = analysis_results["summary"]
    print(
        f"[Agente Analista] Tipo: {dtype} | Anomalías: {n_anomalies} | "
        f"Resumen: {summary}"
    )

    dataset_id = state.get("dataset_id") or settings.default_dataset_id
    try:
        path = save_analysis_data(dataset_id, analysis_results)
        print(f"[Agente Analista] Análisis guardado en: {path}")
    except Exception as exc:
        print(f"[Agente Analista] Advertencia: no se pudo guardar el análisis: {exc}")

    return {**state, "analysis": analysis_results}
