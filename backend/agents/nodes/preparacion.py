from backend.agents.state import AgentState
from backend.agents.tools.data_tools import clean_health_data
from backend.core.config import settings
from backend.core.storage import save_clean_data


def preparacion_node(state: AgentState) -> AgentState:
    raw_data = state.get("data")

    if not raw_data:
        print("[Agente de Preparación] Advertencia: no hay datos para limpiar.")
        return state

    print("[Agente de Preparación] Iniciando limpieza de datos con Pandas...")

    try:
        df_clean = clean_health_data(raw_data)
    except Exception as exc:
        print(f"[Agente de Preparación] Error durante la limpieza: {exc}")
        return state

    rows, cols = df_clean.shape
    print(
        f"[Agente de Preparación] Limpieza completa. Filas: {rows} | Columnas: {cols}"
    )

    dataset_id = state.get("dataset_id") or settings.default_dataset_id
    try:
        path = save_clean_data(dataset_id, df_clean)
        print(f"[Agente de Preparación] Dataset limpio guardado en: {path}")
    except Exception as exc:
        print(
            f"[Agente de Preparación] Advertencia: no se pudo guardar el CSV limpio: {exc}"
        )

    return {**state, "data": df_clean}
