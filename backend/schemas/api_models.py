from __future__ import annotations

from pydantic import BaseModel


class RunRequest(BaseModel):
    query: str


class RunResponse(BaseModel):
    insights: list[str] = []
    alerts: list[str] = []

