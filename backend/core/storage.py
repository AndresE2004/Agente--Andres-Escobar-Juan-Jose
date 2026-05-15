from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"
ANALYSIS_DIR = DATA_DIR / "analysis"


def _ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def save_raw_data(dataset_id: str, data: list[dict[str, Any]]) -> Path:
    """Guarda los datos crudos como JSON en data/raw/<dataset_id>.json."""
    _ensure_dirs()
    path = RAW_DIR / f"{dataset_id}.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    return path


def save_clean_data(dataset_id: str, df: pd.DataFrame) -> Path:
    """Guarda el DataFrame limpio como CSV en data/clean/<dataset_id>.csv."""
    _ensure_dirs()
    path = CLEAN_DIR / f"{dataset_id}.csv"
    df.to_csv(path, index=False, encoding="utf-8")
    return path


def save_analysis_data(dataset_id: str, analysis: dict[str, Any]) -> Path:
    """Guarda el resultado del análisis en data/analysis/<dataset_id>.json."""
    _ensure_dirs()
    path = ANALYSIS_DIR / f"{dataset_id}.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(analysis, fh, ensure_ascii=False, indent=2, default=str)
    return path


def load_raw_data(dataset_id: str) -> list[dict[str, Any]] | None:
    """Carga datos crudos desde data/raw/<dataset_id>.json si existe."""
    path = RAW_DIR / f"{dataset_id}.json"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_clean_data(dataset_id: str) -> pd.DataFrame | None:
    """Carga el DataFrame limpio desde data/clean/<dataset_id>.csv si existe."""
    path = CLEAN_DIR / f"{dataset_id}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)
