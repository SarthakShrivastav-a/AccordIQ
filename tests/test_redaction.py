from accordiq.core.redaction import redact_text

def test_redacts_email():
    result = redact_text("mail me at a@example.com", {"email": r"\b\S+@\S+\.\S+\b"}, ["email"])
    assert "[REDACTED]" in result.text
    assert result.count == 1
