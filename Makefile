.PHONY: test install install-global uninstall-global
.PHONY: pre-commit-install pre-commit-run
.PHONY: sharebanner

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

# Generate share-banner.png from share-banner.svg (SVG can be generated/updated with AI requests)
sharebanner: share-banner.png

share-banner.png: share-banner.svg
	inkscape --export-type=png $<
