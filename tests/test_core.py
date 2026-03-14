"""Tests for sigillin.core – Sigil trilayer loading and CREP validation."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import numpy as np
import pytest

from sigillin.core import Sigil, SigilValidationError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_CREP = {
    "coherence": 0.9,
    "resonance": 0.8,
    "emergence": 0.7,
    "poetics": "The light bends toward itself.",
}

PARTIAL_CREP = {
    "coherence": 0.9,
    "resonance": 0.8,
}


@pytest.fixture
def valid_yaml_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "test.yaml"
    import yaml
    p.write_text(yaml.dump(VALID_CREP), encoding="utf-8")
    return p


@pytest.fixture
def partial_yaml_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "partial.yaml"
    import yaml
    p.write_text(yaml.dump(PARTIAL_CREP), encoding="utf-8")
    return p


@pytest.fixture
def valid_json_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "test.json"
    p.write_text(json.dumps(VALID_CREP), encoding="utf-8")
    return p


@pytest.fixture
def valid_md_sigil(tmp_path: Path) -> Path:
    p = tmp_path / "test.md"
    content = textwrap.dedent("""\
        ---
        coherence: 0.9
        resonance: 0.8
        emergence: 0.7
        poetics: The light bends toward itself.
        ---
        # Narrative

        Full poetic description here.
    """)
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Trilayer loading
# ---------------------------------------------------------------------------


def test_load_yaml(valid_yaml_sigil: Path) -> None:
    sigil = Sigil(valid_yaml_sigil)
    assert sigil.data["coherence"] == pytest.approx(0.9)


def test_load_json(valid_json_sigil: Path) -> None:
    sigil = Sigil(valid_json_sigil)
    assert sigil.data["coherence"] == pytest.approx(0.9)


def test_load_markdown_frontmatter(valid_md_sigil: Path) -> None:
    sigil = Sigil(valid_md_sigil)
    assert sigil.data["emergence"] == pytest.approx(0.7)
    assert "poetics" in sigil.data


def test_empty_yaml(tmp_path: Path) -> None:
    p = tmp_path / "empty.yaml"
    p.write_text("", encoding="utf-8")
    sigil = Sigil(p)
    assert sigil.data == {}


def test_md_without_frontmatter(tmp_path: Path) -> None:
    p = tmp_path / "plain.md"
    p.write_text("# No front-matter\nJust prose.", encoding="utf-8")
    sigil = Sigil(p)
    assert sigil.data == {}


# ---------------------------------------------------------------------------
# CREP validation
# ---------------------------------------------------------------------------


def test_validate_crep_true(valid_yaml_sigil: Path) -> None:
    assert Sigil(valid_yaml_sigil).validate_crep() is True


def test_validate_crep_false(partial_yaml_sigil: Path) -> None:
    assert Sigil(partial_yaml_sigil).validate_crep() is False


def test_assert_crep_passes(valid_yaml_sigil: Path) -> None:
    Sigil(valid_yaml_sigil).assert_crep()  # must not raise


def test_assert_crep_raises(partial_yaml_sigil: Path) -> None:
    with pytest.raises(SigilValidationError, match="missing CREP keys"):
        Sigil(partial_yaml_sigil).assert_crep()


# ---------------------------------------------------------------------------
# MandalaMap resonance
# ---------------------------------------------------------------------------


def test_render_mandala_shape(valid_yaml_sigil: Path) -> None:
    spectrum = Sigil(valid_yaml_sigil).render_mandala()
    assert isinstance(spectrum, np.ndarray)
    assert spectrum.shape == (100,)


def test_render_mandala_phi_depth(valid_yaml_sigil: Path) -> None:
    spectrum = Sigil(valid_yaml_sigil).render_mandala(depth=0.618)
    assert spectrum.max() == pytest.approx(1.618, abs=0.001)


def test_render_mandala_custom_depth(valid_yaml_sigil: Path) -> None:
    s1 = Sigil(valid_yaml_sigil).render_mandala(depth=0.1)
    s2 = Sigil(valid_yaml_sigil).render_mandala(depth=1.0)
    assert not np.allclose(s1, s2)


# ---------------------------------------------------------------------------
# Optional fieldtheory binding
# ---------------------------------------------------------------------------


def test_bind_to_field_without_stack(valid_yaml_sigil: Path) -> None:
    result = Sigil(valid_yaml_sigil).bind_to_field()
    # fieldtheory is not installed in the test environment
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# Dunder helpers
# ---------------------------------------------------------------------------


def test_repr(valid_yaml_sigil: Path) -> None:
    sigil = Sigil(valid_yaml_sigil)
    r = repr(sigil)
    assert "Sigil" in r
    assert "crep_valid=True" in r


def test_getitem(valid_yaml_sigil: Path) -> None:
    sigil = Sigil(valid_yaml_sigil)
    assert sigil["coherence"] == pytest.approx(0.9)


def test_get_default(valid_yaml_sigil: Path) -> None:
    sigil = Sigil(valid_yaml_sigil)
    assert sigil.get("nonexistent", "default") == "default"
