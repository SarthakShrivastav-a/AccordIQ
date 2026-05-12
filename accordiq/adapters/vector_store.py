from __future__ import annotations

import math

def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)

def hybrid_score(vector_score: float, keyword_score: float, recency_score: float) -> float:
    return 0.65 * vector_score + 0.25 * keyword_score + 0.10 * recency_score
