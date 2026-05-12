import hashlib, hmac, time
from accordiq.core.security import deterministic_id, verify_slack_signature

def test_slack_signature_valid():
    body = b'{"type":"event_callback"}'
    ts = str(int(time.time()))
    base = b"v0:" + ts.encode() + b":" + body
    sig = "v0=" + hmac.new(b"secret", base, hashlib.sha256).hexdigest()
    assert verify_slack_signature(body, ts, sig, "secret", 300)

def test_deterministic_id_stable():
    assert deterministic_id("a", "b") == deterministic_id("a", "b")
