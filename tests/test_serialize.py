from datetime import datetime, timezone

from telegram_reader.serialize import _to_local_human, message_to_markdown_block


class StubMessage:
    def __init__(self, message: str, date: datetime | None) -> None:
        self.message = message
        self.date = date


def test_to_local_human_formats_without_seconds():
    dt = datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    human = _to_local_human(dt)
    # Expect format YYYY-MM-DD HH:MM
    assert len(human) == 16
    assert human[4] == "-" and human[7] == "-" and human[10] == " " and human[13] == ":"


def test_message_to_markdown_block_includes_header_and_body():
    m = StubMessage("Hello world", datetime(2024, 1, 2, 3, 4, tzinfo=timezone.utc))
    block = message_to_markdown_block(m)  # type: ignore[arg-type]
    assert block is not None
    assert block.startswith("## ")
    assert "Hello world" in block


def test_message_to_markdown_block_skips_empty():
    m1 = StubMessage("", datetime.now(timezone.utc))
    m2 = StubMessage("   \n\t", datetime.now(timezone.utc))
    assert message_to_markdown_block(m1) is None  # type: ignore[arg-type]
    assert message_to_markdown_block(m2) is None  # type: ignore[arg-type]

