from accordiq.services.entity_service import build_accordiq_id, route_entity_status

def test_entity_id_prefix():
    assert build_accordiq_id("W", "1", "task", "Ship").startswith("acc_")

def test_review_routing():
    assert route_entity_status(0.4, 0.55) == "review"
    assert route_entity_status(0.8, 0.55) == "active"
