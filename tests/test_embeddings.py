from accordiq.adapters.embeddings import deterministic_embedding

def test_embedding_dimensions():
    assert len(deterministic_embedding("hello", 12)) == 12
