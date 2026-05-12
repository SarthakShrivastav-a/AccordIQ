from accordiq.core.config import load_settings

def test_load_settings():
    settings = load_settings("config/app.yaml")
    assert settings.app.name == "AccordIQ"
    assert settings.docker.image_repository == "sarthak73/accordiq"
