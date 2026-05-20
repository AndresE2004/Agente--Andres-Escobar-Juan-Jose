## Uso de APIs de datos abiertos en salud mediante agentes autónomos

Este proyecto consume una API de datos abiertos (p. ej. `datos.gov.co`) con información del sector salud. **Agentes autónomos** descargan, limpian, analizan y generan informes en lenguaje natural sobre esos datos.

## Stack

- **Python** + **LangGraph** (orquestación)
- **Pandas / NumPy** (preparación y análisis)
- **Ollama** (LLM local para insights, Sprint 4)
- **FastAPI** (backend, endpoints básicos)
- **Streamlit** (frontend base, pendiente de integración completa)

## Estado del proyecto

| Sprint | Agente        | Estado        | CLI (`run.py`)                    |
|--------|---------------|---------------|-----------------------------------|
| 1      | Ingesta       | Implementado  | `--mode ingesta`                  |
| 2      | Preparación   | Implementado  | `--mode preparacion`              |
| 3      | Analista      | Implementado  | `--mode analista`                 |
| 4      | Insights      | Implementado  | Solo dentro de `--mode all`       |
| 5      | Alertas       | Placeholder   | Se ejecuta en `--mode all` sin lógica |

Pipeline (LangGraph):

`ingesta` → `preparacion` → `analista` → `insights` → `alertas`

---

## Requisitos previos

- **Python 3.10+**
- Conexión a internet (descarga desde datos.gov.co)
- **Ollama** (solo si quieres Sprint 4: informe en lenguaje natural)

---

## Instalación del proyecto

### 1) Clonar / abrir el repo y crear entorno virtual

**Windows (PowerShell):**

```powershell
cd "ruta\al\proyecto\Agente--Andres-Escobar-Juan-Jose"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / Mac:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Variables de entorno

```powershell
copy .env.example .env
```

| Variable            | Descripción                          | Por defecto      |
|---------------------|--------------------------------------|------------------|
| `SOCRATA_DOMAIN`    | Dominio Socrata                      | `datos.gov.co`   |
| `SOCRATA_APP_TOKEN` | Token opcional (recomendado)         | vacío            |
| `DEFAULT_DATASET_ID`| Dataset por defecto                  | `hn4i-593p`      |

---

## Instalación de Ollama (Sprint 4)

El Agente de Insights usa un modelo local (`llama3`) vía [Ollama](https://ollama.com). Sin Ollama, los Sprints 1–3 siguen funcionando; el informe en lenguaje natural no se generará.

### Windows

1. Descarga el instalador: https://ollama.com/download  
2. Instala Ollama y **cierra y vuelve a abrir** la terminal (PowerShell o Cursor).  
3. Verifica la instalación:

```powershell
ollama --version
```

Si aparece `CommandNotFoundException`, Ollama no está en el PATH. Prueba con la ruta completa:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```

4. Descarga el modelo (puede tardar varios minutos):

```powershell
ollama pull llama3
```

5. Ollama en Windows suele iniciarse solo al instalar (icono en la bandeja). No suele hacer falta `ollama serve` manualmente. Si `pull` falla, abre la app **Ollama** desde el menú Inicio.

### Linux / Mac

```bash
# Instalación: ver https://ollama.com/download
ollama pull llama3
```

### Comprobar que Ollama responde

```powershell
ollama list
```

Debe aparecer `llama3` en la lista.

---

## Guía rápida: ejecutar todo lo implementado

Con el entorno activado y Ollama instalado (para Sprint 4):

```powershell
python run.py --mode all --dataset all
```

Eso procesa **los tres datasets** en secuencia: afiliados, sivigila e ips.

Un solo dataset:

```powershell
python run.py --mode all --dataset afiliados
```

### Qué hace `--mode all`

Por cada dataset ejecuta:

1. **Ingesta** — descarga desde Socrata (máx. 500 registros por prueba)  
2. **Preparación** — limpieza con Pandas  
3. **Analista** — estadísticas y detección de anomalías  
4. **Insights** — informe en español con Ollama (si está activo)  
5. **Alertas** — nodo placeholder (sin lógica aún)

### Archivos que se generan (por dataset)

Los archivos se **sobrescriben** en cada ejecución (no hay versionado con fecha):

```
data/raw/<dataset_id>.json        # Sprint 1 — datos crudos
data/clean/<dataset_id>.csv       # Sprint 2 — datos limpios
data/analysis/<dataset_id>.json   # Sprint 3 — resumen + anomalías
```

Los **insights** (Sprint 4) se guardan en `data/insights/<dataset_id>.txt`. El JSON de análisis incluye `metric_note` y cada anomalía trae un campo `ubicacion` fijo. Ollama responde solo en español; si el informe no coincide con los datos, se reintenta automáticamente y se valida antes de guardar.

Ejemplo para afiliados (`hn4i-593p`):

```
data/raw/hn4i-593p.json
data/clean/hn4i-593p.csv
data/analysis/hn4i-593p.json
```

---

## Datasets disponibles

| Alias CLI   | ID Socrata   | Descripción           | Columna analizada (Sprint 3) |
|-------------|--------------|-----------------------|------------------------------|
| `afiliados` | `hn4i-593p`  | Afiliados a Salud     | `numpersonas`                |
| `sivigila`  | `4hyg-wa9d`  | SIVIGILA              | `conteo`                     |
| `ips`       | `ugc5-acjp`  | Sedes IPS             | conteo por `depa_nombre`     |
| `all`       | los tres     | Procesa los 3         | —                            |

---

## Ejecutar por Sprint (validación por partes)

Todos los comandos usan `run.py`. Activa el venv antes de ejecutar.

### Sprint 1 — Ingesta

```powershell
python run.py --mode ingesta --dataset afiliados
python run.py --mode ingesta --dataset all
```

Salida: `data/raw/<dataset_id>.json`

### Sprint 2 — Preparación

Reutiliza el JSON crudo si existe; si no, ejecuta ingesta primero.

```powershell
python run.py --mode preparacion --dataset afiliados
python run.py --mode preparacion --dataset all
```

Salida: `data/clean/<dataset_id>.csv`

### Sprint 3 — Analista

Reutiliza el CSV limpio si existe; si no, ejecuta ingesta y preparación primero.

```powershell
python run.py --mode analista --dataset afiliados
python run.py --mode analista --dataset sivigila
python run.py --mode analista --dataset all
```

Salida: `data/analysis/<dataset_id>.json`

### Sprint 4 — Insights (Ollama)

No tiene modo CLI propio. Se ejecuta automáticamente al final de:

```powershell
python run.py --mode all --dataset afiliados
```

Requiere Ollama en ejecución y el modelo `llama3` descargado.

---

## Estructura del repositorio

```
.
├── backend/
│   ├── main.py
│   ├── api/
│   ├── core/           # config, socrata, storage
│   ├── agents/
│   │   ├── graph.py
│   │   ├── nodes/      # ingesta, preparacion, analista, insights, alertas
│   │   └── tools/
│   └── prompts/
├── data/
│   ├── raw/
│   ├── clean/
│   └── analysis/
├── frontend/
├── run.py              # CLI principal
├── tests/
└── requirements.txt
```

---

## Tests automatizados

```powershell
pytest -q
```

Por sprint:

```powershell
pytest tests/test_ingesta.py -q
pytest tests/test_preparacion.py -q
pytest tests/test_graph.py -q
```

---

## Backend y frontend (uso futuro)

El flujo multiagente **no** se expone aún por HTTP. Eso está previsto para el Sprint 5.

Por ahora solo hay endpoints de prueba:

```powershell
uvicorn backend.main:app --reload
```

```powershell
streamlit run frontend/app.py
```

---

## Solución de problemas

| Problema | Qué hacer |
|----------|-----------|
| `'ollama' no se reconoce` | Instalar Ollama desde https://ollama.com/download y reiniciar la terminal |
| Error conexión `localhost:11434` | Abrir la app Ollama o ejecutar `ollama serve` |
| `ModuleNotFoundError: langchain_community` | `pip install -r requirements.txt` |
| Ollama inventa datos en IPS | Re-ejecutar tras actualizar: IPS ahora se analiza por departamento |
| Archivos viejos desaparecen | Cada corrida sobrescribe `data/raw`, `data/clean` y `data/analysis` del mismo `dataset_id` |

---

## Referencia rápida de comandos

| Objetivo | Comando |
|----------|---------|
| Todo (3 datasets, Sprints 1–4) | `python run.py --mode all --dataset all` |
| Todo (1 dataset) | `python run.py --mode all --dataset afiliados` |
| Solo descargar datos | `python run.py --mode ingesta --dataset all` |
| Solo limpiar | `python run.py --mode preparacion --dataset afiliados` |
| Solo analizar | `python run.py --mode analista --dataset sivigila` |
| Tests | `pytest -q` |
