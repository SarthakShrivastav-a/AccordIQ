from typing_extensions import TypedDict

class ExtractionState(TypedDict, total=False):
    workspace_id: str
    message_id: str
    text: str
    source: dict
    entities: list[dict]
    confidence: float
    status: str
    errors: list[str]
