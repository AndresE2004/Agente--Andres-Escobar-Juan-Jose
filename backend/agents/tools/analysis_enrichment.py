from __future__ import annotations


def enrich_anomaly_record(record: dict, dataset_type: str) -> dict:
    """Añade campo 'ubicacion' legible para que el LLM no confunda filas."""
    enriched = dict(record)

    if dataset_type == "afiliados":
        enriched["ubicacion"] = (
            f"{record.get('municipio', 'N/D')}, {record.get('departamento', 'N/D')}, "
            f"mes {record.get('mes')}/{record.get('ano')}, "
            f"numpersonas: {record.get('numpersonas')}"
        )
    elif dataset_type == "sivigila":
        enriched["ubicacion"] = (
            f"{record.get('departamento_ocurrencia', 'N/D')}, "
            f"{record.get('municipio_ocurrencia', 'N/D')}, "
            f"semana {record.get('semana')} año {record.get('ano')}, "
            f"evento: {record.get('nombre_evento', 'N/D')}, "
            f"conteo: {record.get('conteo')}"
        )
    elif dataset_type == "ips":
        enriched["ubicacion"] = (
            f"Departamento {record.get('depa_nombre', 'N/D')}, "
            f"conteo_ips: {record.get('conteo_ips')}"
        )
    else:
        enriched["ubicacion"] = str(record)

    return enriched


def enrich_anomalies(anomalies: list[dict], dataset_type: str) -> list[dict]:
    return [enrich_anomaly_record(row, dataset_type) for row in anomalies]
