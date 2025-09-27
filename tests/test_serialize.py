from datetime import datetime, timezone

from telegram_reader.serialize import message_to_markdown_block
from telethon.tl.types import PeerUser, PeerChannel


class StubSender:
    def __init__(self, username=None, first_name=None, last_name=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class StubMessage:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def _now():
    return datetime(2025, 9, 27, 12, 0, tzinfo=timezone.utc)


def test_markdown_includes_me_for_outgoing():
    m = StubMessage(message="hello", date=_now(), out=True)
    md = message_to_markdown_block(m)
    assert md is not None
    assert "— ME" in md.splitlines()[0]


def test_markdown_includes_username_and_not_id_when_username_present():
    m = StubMessage(
        message="hi",
        date=_now(),
        out=False,
        from_id=PeerUser(user_id=42),
        sender=StubSender(username="alice", first_name="Alice", last_name="L"),
    )
    md = message_to_markdown_block(m)
    head = md.splitlines()[0]
    # Shows full name and @username
    assert "Alice L (" in head and "@alice" in head
    # Does not append [user 42] because username exists
    assert "[user 42]" not in head


def test_markdown_includes_id_when_no_username():
    m = StubMessage(
        message="hey",
        date=_now(),
        out=False,
        from_id=PeerUser(user_id=99),
        sender=StubSender(username=None, first_name="Bob", last_name=None),
    )
    md = message_to_markdown_block(m)
    head = md.splitlines()[0]
    assert "Bob" in head
    assert "[user 99]" in head


def test_channel_posts_include_channel_id_and_post_author_when_present():
    m = StubMessage(
        message="post",
        date=_now(),
        out=False,
        from_id=PeerChannel(channel_id=777),
        sender=None,
        post_author="Moderator",
    )
    md = message_to_markdown_block(m)
    head = md.splitlines()[0]
    assert "channel 777" in head
    assert "[channel 777]" in head
    assert "Moderator" in head
