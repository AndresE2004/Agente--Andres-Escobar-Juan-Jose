from __future__ import annotations

import httpx

from backend.core.config import settings


class SocrataClient:
    def __init__(self, domain: str | None = None, app_token: str | None = None):
        self.domain = domain or settings.socrata_domain
        self.app_token = app_token or settings.socrata_app_token

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.app_token:
            headers["X-App-Token"] = self.app_token
        return headers

    async def get(self, path: str, params: dict | None = None) -> dict | list:
        url = f"https://{self.domain}{path}"
        async with httpx.AsyncClient(headers=self._headers(), timeout=30) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()

