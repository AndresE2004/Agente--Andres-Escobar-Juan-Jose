from backend.agents.tools.analysis_enrichment import enrich_anomalies
from backend.agents.tools.insights_validation import validate_insights_report


def test_enrich_sivigila_anomaly_has_ubicacion():
    row = {
        "departamento_ocurrencia": "BOGOTA",
        "municipio_ocurrencia": "BOGOTA",
        "semana": 34,
        "ano": 2019,
        "nombre_evento": "BAJO PESO AL NACER",
        "conteo": 95,
    }
    enriched = enrich_anomalies([row], "sivigila")[0]
    assert "ubicacion" in enriched
    assert "BOGOTA" in enriched["ubicacion"]
    assert "95" in enriched["ubicacion"]


def test_validate_detects_wrong_department():
    analysis = {
        "dataset_type": "sivigila",
        "summary": {"promedio": 2.996, "max": 107, "min": 1, "n": 500},
        "anomalies": enrich_anomalies(
            [
                {
                    "departamento_ocurrencia": "BOGOTA",
                    "municipio_ocurrencia": "BOGOTA",
                    "semana": 34,
                    "ano": 2019,
                    "nombre_evento": "BAJO PESO AL NACER",
                    "conteo": 95,
                }
            ],
            "sivigila",
        ),
    }
    bad_report = "En Antioquia, Medellín, semana 34 de 2019 se registraron 95 casos."
    ok, errors = validate_insights_report(analysis, bad_report)
    assert not ok
    assert len(errors) > 0


def test_validate_accepts_correct_report():
    analysis = {
        "dataset_type": "sivigila",
        "summary": {"promedio": 2.996, "max": 107, "min": 1, "n": 500},
        "anomalies": enrich_anomalies(
            [
                {
                    "departamento_ocurrencia": "BOGOTA",
                    "municipio_ocurrencia": "BOGOTA",
                    "semana": 34,
                    "ano": 2019,
                    "nombre_evento": "BAJO PESO AL NACER",
                    "conteo": 95,
                }
            ],
            "sivigila",
        ),
    }
    good_report = (
        "Muestra de 500 registros. Promedio 2.996, máximo 107. "
        "Anomalía: BOGOTA, BOGOTA, semana 34 año 2019, evento: BAJO PESO AL NACER, conteo: 95."
    )
    ok, errors = validate_insights_report(analysis, good_report)
    assert ok
    assert errors == []
