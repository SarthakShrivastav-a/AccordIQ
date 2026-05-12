from accordiq.adapters.vector_store import cosine_similarity, hybrid_score

def test_cosine_similarity():
    assert cosine_similarity([1, 0], [1, 0]) == 1

def test_hybrid_score():
    assert hybrid_score(1, 0, 0) == 0.65
