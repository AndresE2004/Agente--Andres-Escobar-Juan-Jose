import asyncio
from typing import Any

from backend.agents.state import AgentState
from backend.core.config import settings
from backend.core.socrata_client import SocrataClient


async def fetch_data(dataset_id: str) -> list[dict[str, Any]]:
    client = SocrataClient()
    data = await client.get(f"/resource/{dataset_id}.json", params={"$limit": 500})
    if isinstance(data, list):
        return data
    return [data]


def ingesta_node(state: AgentState) -> AgentState:
    print(f"[ingesta] Iniciando descarga desde Socrata dataset={settings.default_dataset_id} ...")
    rows = asyncio.run(fetch_data(settings.default_dataset_id))
    print(f"[ingesta] Descarga completa. Registros descargados: {len(rows)}")
    return {**state, "data": rows}

