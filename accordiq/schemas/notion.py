from pydantic import BaseModel

class NotionPageRef(BaseModel):
    page_id: str
    url: str | None = None
    data_source_id: str | None = None
