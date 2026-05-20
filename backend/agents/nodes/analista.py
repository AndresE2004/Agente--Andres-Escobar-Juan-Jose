from __future__ import annotations

import pandas as pd

from backend.agents.state import AgentState
from backend.agents.tools.analysis_enrichment import enrich_anomalies
from backend.agents.tools.math_tools import (
    analyze_ips_by_department,
    calculate_trend_summary,
    detect_anomalies,
)
from backend.core.config import settings
from backend.core.storage import save_analysis_data

DATASET_VALUE_COLUMNS: dict[str, str] = {
    "afiliados": "numpersonas",
    "sivigila": "conteo",
}

METRIC_NOTES: dict[str, str] = {
    "afiliados": (
        "El campo 'total' es la SUMA de 'numpersonas' en las filas del extracto "
        "(municipio/mes), NO es el total de afiliados únicos en Colombia."
    ),
    "sivigila": (
        "El campo 'total' es la SUMA de 'conteo' en las filas del extracto "
        "(evento/semana/municipio), NO es el total nacional del evento."
    ),
    "ips": (
        "Se analiza la cantidad de registros IPS por departamento en el extracto. "
        "Las anomalías son departamentos con concentración inusualmente alta."
    ),
}


def _detect_dataset_type(df: pd.DataFrame) -> str | None:
    if "numpersonas" in df.columns:
        return "afiliados"
    if "conteo" in df.columns:
        return "sivigila"
    if "depa_nombre" in df.columns and "codigo_habilitacion" in df.columns:
        return "ips"
    return None


def analista_node(state: AgentState) -> AgentState:
    df = state.get("data")

    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        print("[Agente Analista] Advertencia: no hay DataFrame válido para analizar.")
        return state

    print("[Agente Analista] Iniciando análisis estadístico...")

    dataset_type = _detect_dataset_type(df)
    analysis_results: dict = {
        "dataset_type": dataset_type or "unknown",
        "column_analyzed": None,
        "rows_in_sample": len(df),
        "metric_note": "",
        "summary": {},
        "anomalies": [],
    }

    try:
        if dataset_type == "ips":
            summary, anomalies = analyze_ips_by_department(df)
            analysis_results["column_analyzed"] = "conteo por depa_nombre"
            analysis_results["summary"] = summary
            analysis_results["anomalies"] = anomalies
            analysis_results["metric_note"] = METRIC_NOTES["ips"]
        elif dataset_type in DATASET_VALUE_COLUMNS:
            value_col = DATASET_VALUE_COLUMNS[dataset_type]
            analysis_results["column_analyzed"] = value_col
            analysis_results["summary"] = calculate_trend_summary(df, value_col)
            analysis_results["anomalies"] = detect_anomalies(df, value_col)
            analysis_results["metric_note"] = METRIC_NOTES[dataset_type]
        else:
            print("[Agente Analista] No se reconoció un esquema de dataset analizable.")

        dtype = analysis_results["dataset_type"]
        if dtype and dtype != "unknown":
            enriched = enrich_anomalies(analysis_results["anomalies"], dtype)
            analysis_results["anomalies"] = enriched
            analysis_results["anomalies_detalle"] = [
                row.get("ubicacion", "") for row in enriched
            ]
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
