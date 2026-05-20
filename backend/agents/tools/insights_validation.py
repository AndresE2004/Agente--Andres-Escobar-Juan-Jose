from __future__ import annotations

import re
import unicodedata


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def _value_in_report(value: object, report: str) -> bool:
    if value is None:
        return True
    raw = str(value)
    if raw in report:
        return True
    if isinstance(value, float) and value.is_integer():
        return str(int(value)) in report
    return False


def _location_tokens_in_report(record: dict, dataset_type: str, report_norm: str) -> bool:
    if dataset_type == "afiliados":
        tokens = [record.get("departamento"), record.get("municipio")]
    elif dataset_type == "sivigila":
        tokens = [
            record.get("departamento_ocurrencia"),
            record.get("municipio_ocurrencia"),
        ]
    elif dataset_type == "ips":
        tokens = [record.get("depa_nombre")]
    else:
        return True

    for token in tokens:
        if token and _normalize(str(token)) not in report_norm:
            return False
    return True


def validate_insights_report(analysis: dict, report: str) -> tuple[bool, list[str]]:
    """Comprueba que el informe refleje valores y ubicaciones del JSON de análisis."""
    errors: list[str] = []
    report_norm = _normalize(report)
    dataset_type = analysis.get("dataset_type", "unknown")
    anomalies = analysis.get("anomalies") or []

    summary = analysis.get("summary") or {}
    for key in ("promedio", "max", "min", "total"):
        if key in summary and not _value_in_report(summary[key], report):
            errors.append(f"El valor de summary['{key}']={summary[key]} no aparece en el informe.")

    for idx, row in enumerate(anomalies, start=1):
        ubicacion = row.get("ubicacion", f"anomalía {idx}")

        value_key = None
        for candidate in ("conteo", "numpersonas", "conteo_ips"):
            if candidate in row:
                value_key = candidate
                break

        if value_key and not _value_in_report(row[value_key], report):
            errors.append(
                f"Anomalía {idx}: el valor {value_key}={row[value_key]} no está en el informe. "
                f"Referencia: {ubicacion}"
            )

        if not _location_tokens_in_report(row, dataset_type, report_norm):
            errors.append(
                f"Anomalía {idx}: departamento/municipio no coinciden con el informe. "
                f"Usar exactamente: {ubicacion}"
            )

        ubicacion_norm = _normalize(ubicacion)
        if len(ubicacion_norm) > 20 and ubicacion_norm not in report_norm:
            if re.search(r"\d+", ubicacion):
                pass
            else:
                errors.append(
                    f"Anomalía {idx}: el texto de ubicacion no se refleja. Copiar: {ubicacion}"
                )

    return len(errors) == 0, errors
