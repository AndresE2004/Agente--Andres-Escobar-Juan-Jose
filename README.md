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

> **Estado actual:** Sprints 1, 2 y 3 implementados. Los nodos `insights` y `alertas` aún son placeholders.

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
├── data/
│   ├── raw/        # Salida Sprint 1 (JSON crudo)
│   ├── clean/      # Salida Sprint 2 (CSV limpio)
│   └── analysis/   # Salida Sprint 3 (JSON con análisis)
├── frontend/
│   ├── app.py
│   ├── pages/
│   └── components/
├── run.py          # CLI principal para ejecutar agentes
├── tests/
└── requirements.txt
```

## Datasets disponibles

| Alias CLI   | ID Socrata   | Descripción              |
|-------------|--------------|--------------------------|
| `afiliados` | `hn4i-593p`  | Afiliados a Salud        |
| `sivigila`  | `4hyg-wa9d`  | Vigilancia (SIVIGILA)    |
| `ips`       | `ugc5-acjp`  | Sedes de Salud (IPS)     |
| `all`       | (los tres)   | Procesa los 3 datasets   |

## Ejecución (sugerida)

### 1) Crear entorno e instalar dependencias

En Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux/Mac:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configurar variables de entorno

Copia el ejemplo y ajusta si aplica:
```bash
copy .env.example .env
```

Variables relevantes:
- `SOCRATA_DOMAIN` (por defecto `datos.gov.co`)
- `SOCRATA_APP_TOKEN` (opcional, recomendado)
- `DEFAULT_DATASET_ID` (por defecto `hn4i-593p`)

### 3) Ejecutar por Sprint (por separado)

Usa `run.py` con `--mode` y `--dataset`. Todos los comandos asumen que ya activaste el entorno virtual.

#### Sprint 1 — Agente de Ingesta

Descarga datos reales desde datos.gov.co (Socrata) y los guarda en `data/raw/<dataset_id>.json`.

```bash
python run.py --mode ingesta --dataset afiliados
python run.py --mode ingesta --dataset sivigila
python run.py --mode ingesta --dataset ips
```

**Resultado:** `data/raw/hn4i-593p.json`, `data/raw/4hyg-wa9d.json`, etc.

#### Sprint 2 — Agente de Preparación

Limpia y normaliza los datos con Pandas. Si ya existe el JSON crudo, lo reutiliza; si no, ejecuta ingesta primero.

```bash
python run.py --mode preparacion --dataset afiliados
python run.py --mode preparacion --dataset all
```

**Resultado:** `data/clean/<dataset_id>.csv` (columnas en minúsculas, sin duplicados, tipos numéricos corregidos).

#### Sprint 3 — Agente Analista

Calcula estadísticas y detecta anomalías. Si ya existe el CSV limpio, lo reutiliza; si no, ejecuta ingesta y preparación primero.

```bash
python run.py --mode analista --dataset afiliados
python run.py --mode analista --dataset sivigila
python run.py --mode analista --dataset all
```

**Resultado:** `data/analysis/<dataset_id>.json` con `dataset_type`, `summary` y `anomalies`.

> **Nota:** El dataset `ips` no tiene las columnas `numpersonas` ni `conteo`, por lo que el analista reportará `dataset_type: "unknown"` hasta que se defina su columna de análisis.

---

### 4) Ejecutar todo lo implementado hasta ahora (Sprints 1 + 2 + 3)

Ejecuta la cadena completa **ingesta → preparación → analista** (y pasa por los nodos placeholder de insights/alertas) usando LangGraph:

```bash
# Un solo dataset
python run.py --mode all --dataset afiliados

# Los tres datasets de una vez
python run.py --mode all --dataset all
```

**Archivos generados por dataset:**

```
data/raw/<dataset_id>.json       ← Sprint 1
data/clean/<dataset_id>.csv      ← Sprint 2
data/analysis/<dataset_id>.json  ← Sprint 3
```

---

### 5) Ejecutar servicios (backend / frontend)

> El backend FastAPI (`uvicorn`) aún **no expone** el flujo multiagente por HTTP. Eso está previsto para el Sprint 5. Por ahora usa `run.py` como CLI principal.

Backend (FastAPI):
```bash
uvicorn backend.main:app --reload
```

Frontend (Streamlit):
```bash
streamlit run frontend/app.py
```

### 6) Tests

```bash
pytest -q
```

Pruebas por sprint:

```bash
pytest tests/test_ingesta.py -q        # Sprint 1
pytest tests/test_preparacion.py -q    # Sprint 2
pytest tests/test_graph.py -q          # Grafo compila
```
