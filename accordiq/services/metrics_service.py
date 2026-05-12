from __future__ import annotations

def quality_metrics(extracted: int, accepted: int, answered: int, cited: int) -> dict:
    precision_proxy = accepted / extracted if extracted else 0
    groundedness = cited / answered if answered else 0
    return {"precision_proxy": precision_proxy, "groundedness": groundedness}
