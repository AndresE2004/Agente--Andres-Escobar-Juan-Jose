## Uso de APIs de datos abiertos en salud mediante agentes autónomos

Este proyecto consume una API de datos abiertos (p. ej. `datos.gov.co`) con información del sector salud con actualizaciones periódicas (trimestrales o semestrales).
La idea es que **agentes autónomos** consuman estos datos y se encarguen de analizarlos automáticamente para:
- Detectar cambios importantes en indicadores
- Identificar tendencias
- Encontrar posibles problemas (alertas tempranas)

## Stack
- **Backend**: FastAPI
- **Orquestación de agentes**: LangGraph
- **Frontend**: Streamlit

## Arquitectura (esquema actual)

Flujo lógico:
- **Streamlit (`frontend/`)**: UI para consultar/visualizar resultados
- **FastAPI (`backend/`)**: expone endpoints HTTP y coordina la ejecución
- **LangGraph (`backend/agents/`)**: orquesta el grafo multiagente
- **Fuentes de datos**: Socrata/HTTP (`backend/core/socrata_client.py`) y/o base de datos (`backend/core/database.py`)

Pipeline de agentes (LangGraph):
`ingesta` → `preparacion` → `analista` → `insights` → `alertas`

## Estructura del repo (carpetas principales)

```
.
├── backend/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── nodes/
│   │   └── tools/
│   ├── prompts/
│   └── schemas/
├── frontend/
│   ├── app.py
│   ├── pages/
│   └── components/
├── tests/
└── requirements.txt
```

## Ejecución (sugerida)

Instalar dependencias (idealmente en venv):
```bash
pip install -r requirements.txt
```

Backend:
```bash
uvicorn backend.main:app --reload
```

Frontend:
```bash
streamlit run frontend/app.py
```

Tests:
```bash
pytest -q
```
