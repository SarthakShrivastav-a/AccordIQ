from typing_extensions import TypedDict

class QueryState(TypedDict, total=False):
    workspace_id: str
    user_id: str
    text: str
    intent: str
    retrieved: list[dict]
    answer: str
    citations: list[dict]
    grounded: bool
    rewrite_count: int
