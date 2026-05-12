from accordiq.services.slack_normalizer import chunk_text, normalize_slack_text

def test_normalizes_slack_markup():
    assert normalize_slack_text("hi <@U1> in <#C1|eng>") == "hi @U1 in #eng"

def test_chunks_text():
    assert chunk_text("one two three four", 2, 1) == ["one two", "two three", "three four"]
