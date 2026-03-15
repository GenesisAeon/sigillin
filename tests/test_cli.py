"""Tests for the sigillin CLI (sig)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from sigillin.cli import app

runner = CliRunner()

VALID_CREP = {
    "coherence": 0.9,
    "resonance": 0.8,
    "emergence": 0.7,
    "poetics": "Light bends toward its own source.",
}

PARTIAL_CREP = {
    "coherence": 0.9,
    "resonance": 0.8,
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def valid_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "valid.yaml"
    p.write_text(yaml.dump(VALID_CREP), encoding="utf-8")
    return p


@pytest.fixture
def partial_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "partial.yaml"
    p.write_text(yaml.dump(PARTIAL_CREP), encoding="utf-8")
    return p


@pytest.fixture
def valid_json_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "valid.json"
    p.write_text(json.dumps(VALID_CREP), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# validate command
# ---------------------------------------------------------------------------


def test_validate_valid(valid_sigil: Path) -> None:
    result = runner.invoke(app, ["validate", str(valid_sigil)])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


def test_validate_invalid(partial_sigil: Path) -> None:
    result = runner.invoke(app, ["validate", str(partial_sigil)])
    assert result.exit_code != 0
    assert "invalid" in result.output.lower() or "missing" in result.output.lower()


def test_validate_file_not_found(tmp_path: Path) -> None:
    result = runner.invoke(app, ["validate", str(tmp_path / "missing.yaml")])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_validate_json_sigil(valid_json_sigil: Path) -> None:
    result = runner.invoke(app, ["validate", str(valid_json_sigil)])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


# ---------------------------------------------------------------------------
# render command
# ---------------------------------------------------------------------------


def test_render_valid(valid_sigil: Path) -> None:
    result = runner.invoke(app, ["render", str(valid_sigil)])
    assert result.exit_code == 0
    assert "resonance" in result.output.lower()


def test_render_custom_depth(valid_sigil: Path) -> None:
    result = runner.invoke(app, ["render", str(valid_sigil), "--depth", "1.0"])
    assert result.exit_code == 0
    assert "resonance" in result.output.lower()


def test_render_file_not_found(tmp_path: Path) -> None:
    result = runner.invoke(app, ["render", str(tmp_path / "ghost.yaml")])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# inspect command
# ---------------------------------------------------------------------------


def test_inspect_valid(valid_sigil: Path) -> None:
    result = runner.invoke(app, ["inspect", str(valid_sigil)])
    assert result.exit_code == 0
    assert "coherence" in result.output


def test_inspect_shows_crep_status(valid_sigil: Path) -> None:
    result = runner.invoke(app, ["inspect", str(valid_sigil)])
    assert "crep" in result.output.lower() or "valid" in result.output.lower()


def test_inspect_file_not_found(tmp_path: Path) -> None:
    result = runner.invoke(app, ["inspect", str(tmp_path / "ghost.yaml")])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# bridge command
# ---------------------------------------------------------------------------


def test_bridge_default() -> None:
    result = runner.invoke(app, ["bridge"])
    assert result.exit_code == 0
    assert "openai" in result.output.lower() or "bridge" in result.output.lower()


def test_bridge_custom_provider() -> None:
    result = runner.invoke(app, ["bridge", "anthropic"])
    assert result.exit_code == 0
    assert "anthropic" in result.output.lower()
