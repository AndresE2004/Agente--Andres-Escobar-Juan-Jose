from __future__ import annotations

from typing import Any


def head(data: list[dict[str, Any]], n: int = 5) -> list[dict[str, Any]]:
    return data[:n]

