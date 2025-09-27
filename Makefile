.PHONY: test install install-global uninstall-global
.PHONY: pre-commit-install pre-commit-run

test:
	uv run pytest

install:
	uv pip install -e '.[test]'

install-global:
	uv tool install --force .

uninstall-global:
	uv tool uninstall telegram-reader

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
