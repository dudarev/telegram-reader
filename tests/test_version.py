import tomllib

from telegram_reader import __version__


def test_version_matches_pyproject():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    pj_ver = data["project"]["version"]
    assert __version__ == pj_ver
    assert isinstance(__version__, str) and len(__version__) > 0

