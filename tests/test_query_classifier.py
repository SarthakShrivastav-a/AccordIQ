from accordiq.services.query_classifier import classify_query

def test_status_query():
    assert classify_query("what are my open tasks") == "status"

def test_recall_query():
    assert classify_query("what did we decide about launch") == "recall"
