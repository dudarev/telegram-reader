from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import json

import yaml
import os


PROJECT_NAME = "telegram-reader"
CONFIG_FILENAME_YAML = "config.yaml"
CONFIG_FILENAME_JSON = "config.json"
SESSION_FILENAME = "session.session"


@dataclass
class AppConfig:
    api_id: int
    api_hash: str
    default_limit: int = 10

    @staticmethod
    def from_mapping(data: Dict[str, Any]) -> "AppConfig":
        api_id = int(data["api_id"])
        api_hash = str(data["api_hash"])
        default_limit = int(data.get("default_limit", 10))
        return AppConfig(api_id=api_id, api_hash=api_hash, default_limit=default_limit)


class Paths:
    def __init__(self, appname: str = PROJECT_NAME) -> None:
        self.appname = appname

    @property
    def config_dir(self) -> Path:
        base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
        return Path(base) / self.appname

    @property
    def data_dir(self) -> Path:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
        return Path(base) / self.appname

    @property
    def config_path_yaml(self) -> Path:
        return self.config_dir / CONFIG_FILENAME_YAML

    @property
    def config_path_json(self) -> Path:
        return self.config_dir / CONFIG_FILENAME_JSON

    @property
    def session_path(self) -> Path:
        return self.data_dir / SESSION_FILENAME


def ensure_dirs(paths: Paths) -> None:
    paths.config_dir.mkdir(parents=True, exist_ok=True)
    paths.data_dir.mkdir(parents=True, exist_ok=True)


def load_config(paths: Optional[Paths] = None) -> AppConfig:
    paths = paths or Paths()
    ensure_dirs(paths)

    # Prefer YAML
    if paths.config_path_yaml.exists():
        with paths.config_path_yaml.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
            return AppConfig.from_mapping(data)

    # Fallback to JSON
    if paths.config_path_json.exists():
        with paths.config_path_json.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            return AppConfig.from_mapping(data)

    raise FileNotFoundError(
        f"No config found. Create {paths.config_path_yaml} or {paths.config_path_json}."
    )
