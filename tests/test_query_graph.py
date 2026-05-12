from accordiq.graphs.query.graph import run_query_graph

def test_query_has_citation():
    state = run_query_graph({"workspace_id": "W1", "user_id": "U1", "text": "what did we decide", "retrieved": [{"title": "Source", "url": "https://slack.test/source", "preview": "real message"}]})
    assert state["grounded"] is True
    assert state["citations"]

def test_unknown_refuses():
    state = run_query_graph({"workspace_id": "W1", "user_id": "U1", "text": "unknown"})
    assert state["grounded"] is False
