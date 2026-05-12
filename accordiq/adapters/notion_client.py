from __future__ import annotations

from tenacity import retry, stop_after_attempt, wait_exponential

class NotionClient:
    def __init__(self, token: str | None = None, api_version: str | None = None) -> None:
        self.token = token
        self.api_version = api_version

    async def create_database(self, parent_page_id: str, name: str) -> dict:
        return {"data_source_id": f"ds_{parent_page_id}", "name": name}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.1, min=0.1, max=1))
    async def upsert_entity(self, data_source_id: str, accordiq_id: str, properties: dict) -> dict:
        return {"page_id": f"page_{accordiq_id}", "data_source_id": data_source_id, "properties": properties}
