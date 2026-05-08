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

### 3) Ejecutar el sistema por partes o completo (CLI)

Solo ingesta:
```bash
python run.py --mode ingesta
```
Si quieres analizar el Número de Afiliados, ejecutarás:

```Bash
python run.py --mode ingesta --dataset afiliados
```
Si quieres analizar los datos de Vigilancia Pública (SIVIGILA), ejecutarás:

```Bash
python run.py --mode ingesta --dataset sivigila
```

Y si quieres ver los datos de las Sedes de Salud (IPS):

```Bash
python run.py --mode ingesta --dataset ips
```
Flujo completo (LangGraph)(recomendado):
```bash
python run.py --mode all --dataset all
```

### 4) Ejecutar servicios

Backend (FastAPI):
```bash
uvicorn backend.main:app --reload
```

Frontend (Streamlit):
```bash
streamlit run frontend/app.py
```

### 5) Tests
```bash
pytest -q
```
