# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.1.3] - 2025-09-27

### Changed
- Removed references to JSON output formats from roadmap and agent guidance to keep outputs focused on Markdown.


## [0.1.2] - 2025-09-27

### Changed
- Refactored CLI: split monolithic `cli.py` into per-command modules under `commands/` for maintainability.

### Fixed
- Ensured version command (`tgr version` / `--version`) reports the correct version consistently.


## [0.1.1] - 2025-09-27

### Added
- Fallback peer resolver: numeric `--peer` values now resolve by scanning dialogs when `get_entity` fails.
- Parser `normalize_peer_id` with unit tests.

### Changed
- `messages` command now surfaces a clearer error when a numeric ID isn’t present in dialogs.
- Docs: manual testing guide notes the numeric peer requirement.

### Fixed
- Prevent crash on plain numeric `--peer` by avoiding `get_entity` failure paths.


## [0.1.0] - 2025-09-27

Initial release with basic read-only Telegram CLI functionality.

### Added
- Initial CLI implementation with three commands: `auth`, `dialogs`, and `messages`.
- `auth` command for interactive login and session storage.
- `dialogs` command to list user dialogs (chats, channels, users) with configurable limit.
- `messages` command to read messages from a specific peer (user, chat, or channel) with options for limit, offset, and reverse order.
- Configuration loading from YAML or JSON files in XDG-compliant directories (`~/.config/telegram-reader/`).
- Session management using Telethon's file-based sessions stored in `~/.local/share/telegram-reader/`.
- Markdown output format for messages and dialogs.
- Support for API credentials (api_id and api_hash) via config file.
- Default message limit of 10, configurable via config or command-line.
- Read-only operations; messages are not marked as read.
- Two-step authentication support during login.
- Human-readable timestamps in local timezone for messages.
- Project structure with modular code in `src/telegram_reader/`.
- Entry points for CLI: `telegram-reader` and `tgr`.
- Dependencies: Telethon for Telegram API, PyYAML for config, platformdirs for XDG paths.
