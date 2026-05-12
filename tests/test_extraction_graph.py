from accordiq.graphs.extraction.graph import run_extraction_graph

def test_extracts_task():
    state = run_extraction_graph({"workspace_id": "W1", "text": "I'll send the doc by Friday", "source": {"message_ts": "1"}})
    assert state["entities"][0]["entity_type"] == "task"
    assert state["status"] == "ready"
