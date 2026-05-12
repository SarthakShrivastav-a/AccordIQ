from accordiq.services.capture_policy import should_capture_event

def test_paused_user_skipped():
    ok, reason = should_capture_event({"user": "U1", "text": "hello"}, {"U1"}, set())
    assert not ok
    assert reason == "user_paused"

def test_text_captured():
    ok, reason = should_capture_event({"user": "U2", "text": "I will ship it"}, set(), set())
    assert ok
    assert reason == "capturable"
