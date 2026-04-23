from __future__ import annotations

from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    dataset_id: str
    name: str | None = None

