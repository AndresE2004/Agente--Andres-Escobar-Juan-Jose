from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    query: str
    data: Any
    analysis: Any
    insights: list[str]
    alerts: list[str]

