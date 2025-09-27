from telegram_reader.cli import main


def test_agent_help_output(capsys):
    code = main(["agent"])
    assert code == 0
    out = capsys.readouterr().out
    assert "telegram-reader" in out
    assert "Config" in out
    assert "~/.config/telegram-reader" in out
    assert "Session path" in out
    assert "Dialogs" in out and "messages" in out.lower()
    assert "--peer" in out
    assert "read-only" in out.lower()

