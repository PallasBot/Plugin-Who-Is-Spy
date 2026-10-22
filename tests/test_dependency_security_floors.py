from __future__ import annotations

import importlib.metadata
import re
import tomllib
from pathlib import Path

# 传递依赖安全下限回归：旧解析结果会让本测试失败，升级到下限后通过。
SECURITY_FLOORS: dict[str, str] = {
    "anyio": "4.14.2",
    "msgpack": "1.2.1",
    "multidict": "6.9.1",
}

# 运行时下限必须写入发布 metadata（project.dependencies），否则仅约束本地解析，消费端不受保护。
RUNTIME_FLOORS: dict[str, str] = SECURITY_FLOORS

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"
REQUIREMENT = re.compile(r"^\s*(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*(?P<spec>.*)$")


def parse_version(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for chunk in value.split("."):
        digits = ""
        for char in chunk:
            if not char.isdigit():
                break
            digits += char
        parts.append(int(digits or "0"))
    return tuple(parts)


def declared_floors() -> dict[str, str]:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    floors: dict[str, str] = {}
    for raw in data["project"].get("dependencies", []):
        match = REQUIREMENT.match(raw)
        assert match is not None, raw
        name = match.group("name").lower().replace("_", "-")
        for part in match.group("spec").split(","):
            part = part.strip()
            if part.startswith(">="):
                floors[name] = part[2:].strip()
    return floors


def test_dependency_security_floors() -> None:
    for package, floor in SECURITY_FLOORS.items():
        installed = importlib.metadata.version(package)
        assert parse_version(installed) >= parse_version(floor), f"{package} {installed} < security floor {floor}"


def test_published_metadata_declares_security_floors() -> None:
    floors = declared_floors()
    for package, floor in RUNTIME_FLOORS.items():
        declared = floors.get(package)
        assert declared is not None, f"{package} missing from project.dependencies"
        assert parse_version(declared) >= parse_version(floor), f"{package} {declared} < security floor {floor}"
