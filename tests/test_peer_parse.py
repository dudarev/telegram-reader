from telegram_reader.telethon_client import normalize_peer_id


def test_normalize_plain_digits():
    assert normalize_peer_id("1490343635") == 1490343635


def test_normalize_negative_id():
    assert normalize_peer_id("-12345") == 12345


def test_normalize_channel_style():
    assert normalize_peer_id("-1001234567890") == 1234567890


def test_normalize_non_numeric():
    assert normalize_peer_id("@username") is None
    assert normalize_peer_id("t.me/something") is None
    assert normalize_peer_id("  not-an-id  ") is None

