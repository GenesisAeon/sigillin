"""Tests für sigillin_record — SHA256-Schema, Lineage, Replay."""

from __future__ import annotations

import json

import pytest

from sigillin.sigillin_record import (
    CREPValues,
    NarrativeMetadata,
    Q4StateData,
    SigillinRecord,
    UTACState,
    ValidationResult,
    compute_sigillin_id,
    create_sigillin,
    deserialize_sigillin,
    link_sigillins,
    serialize_sigillin,
    validate_sigillin,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

Q4 = Q4StateData(C=1, R=0, E=1, P=1)   # ID 11 = "1011"
CREP = CREPValues(C=0.82, R=0.44, E=0.91, P=0.87, Gamma=0.736)
UTAC = UTACState(H=0.73, H_star=0.81, K_eff=0.84)
FIXED_TS = "2026-04-19T00:00:00+00:00"


def make_sigil(**kwargs) -> SigillinRecord:
    defaults = dict(
        q4_state=Q4,
        crep=CREP,
        symbolic_identity="heimkehr",
        context="test context",
        intention="test intention",
        cycle=3,
        utac=UTAC,
        timestamp=FIXED_TS,
    )
    defaults.update(kwargs)
    return create_sigillin(**defaults)


# ---------------------------------------------------------------------------
# Q4StateData
# ---------------------------------------------------------------------------

def test_q4_id_calculation() -> None:
    assert Q4StateData(C=1, R=0, E=1, P=1).id == 11
    assert Q4StateData(C=0, R=0, E=0, P=0).id == 0
    assert Q4StateData(C=1, R=1, E=1, P=1).id == 15

def test_q4_binary() -> None:
    assert Q4StateData(C=1, R=0, E=1, P=1).binary == "1011"
    assert Q4StateData(C=0, R=0, E=0, P=0).binary == "0000"

def test_q4_invalid_flag() -> None:
    with pytest.raises(ValueError):
        Q4StateData(C=2, R=0, E=0, P=0)

def test_q4_roundtrip() -> None:
    original = Q4StateData(C=1, R=0, E=1, P=1)
    restored = Q4StateData.from_dict(original.to_dict())
    assert restored == original


# ---------------------------------------------------------------------------
# compute_sigillin_id — deterministisch
# ---------------------------------------------------------------------------

def test_deterministic_id_same_content() -> None:
    """Gleicher Inhalt → gleiche ID (BENCHMARK: deterministic_id)."""
    s1 = make_sigil()
    s2 = make_sigil()
    assert s1.id == s2.id

def test_deterministic_id_different_content() -> None:
    """Verschiedener Inhalt → verschiedene ID."""
    s1 = make_sigil(symbolic_identity="heimkehr")
    s2 = make_sigil(symbolic_identity="abschied")
    assert s1.id != s2.id

def test_id_prefix() -> None:
    s = make_sigil()
    assert s.id.startswith("sig_")

def test_id_excludes_id_field() -> None:
    """compute_sigillin_id ignoriert das 'id'-Feld selbst."""
    content = {"id": "sig_old", "version": "1.0.0", "foo": "bar"}
    id1 = compute_sigillin_id(content)
    content2 = {"id": "sig_other", "version": "1.0.0", "foo": "bar"}
    id2 = compute_sigillin_id(content2)
    assert id1 == id2

def test_id_order_independent() -> None:
    """sort_keys=True → Reihenfolge der Keys ist irrelevant."""
    c1 = {"version": "1.0.0", "foo": "bar", "baz": 1}
    c2 = {"baz": 1, "foo": "bar", "version": "1.0.0"}
    assert compute_sigillin_id(c1) == compute_sigillin_id(c2)


# ---------------------------------------------------------------------------
# Serialize / Deserialize — Roundtrip
# ---------------------------------------------------------------------------

def test_json_roundtrip() -> None:
    """serialize → deserialize reproduziert exakt denselben Record (BENCHMARK: roundtrip_fidelity)."""
    original = make_sigil()
    restored = deserialize_sigillin(serialize_sigillin(original, fmt="json"), fmt="json")
    assert original.id == restored.id
    assert original.symbolic_identity == restored.symbolic_identity
    assert original.q4_state == restored.q4_state
    assert original.crep_values == restored.crep_values
    assert original.utac_state == restored.utac_state
    assert original.semantic_lineage == restored.semantic_lineage

def test_yaml_roundtrip() -> None:
    """YAML-Roundtrip (BENCHMARK: roundtrip_fidelity)."""
    original = make_sigil()
    restored = deserialize_sigillin(serialize_sigillin(original, fmt="yaml"), fmt="yaml")
    assert original.id == restored.id
    assert original.q4_state == restored.q4_state

def test_serialized_json_is_valid_json() -> None:
    s = make_sigil()
    raw = serialize_sigillin(s)
    parsed = json.loads(raw)
    assert parsed["id"] == s.id

def test_deserialized_id_preserved() -> None:
    original = make_sigil()
    raw = serialize_sigillin(original)
    restored = deserialize_sigillin(raw)
    assert restored.id == original.id


# ---------------------------------------------------------------------------
# validate_sigillin — Schema-Validation
# ---------------------------------------------------------------------------

def test_validate_valid_record() -> None:
    """Vollständiger Record ist valide (BENCHMARK: schema_validation)."""
    s = make_sigil()
    result = validate_sigillin(s)
    assert result.valid is True
    assert result.errors == []

def test_validate_bool_coercion() -> None:
    result = validate_sigillin(make_sigil())
    assert bool(result) is True

def test_validate_id_mismatch_detected() -> None:
    """Manipulierte ID wird erkannt."""
    s = make_sigil()
    tampered = SigillinRecord(
        id="sig_tampered0000",
        version=s.version,
        timestamp=s.timestamp,
        symbolic_identity=s.symbolic_identity,
        q4_state=s.q4_state,
        crep_values=s.crep_values,
        narrative_metadata=s.narrative_metadata,
        semantic_lineage=s.semantic_lineage,
        utac_state=s.utac_state,
    )
    result = validate_sigillin(tampered)
    assert result.valid is False
    assert any("ID-Mismatch" in e for e in result.errors)

def test_validate_wrong_version_detected() -> None:
    s = make_sigil()
    broken = SigillinRecord(
        id=s.id,
        version="9.9.9",
        timestamp=s.timestamp,
        symbolic_identity=s.symbolic_identity,
        q4_state=s.q4_state,
        crep_values=s.crep_values,
        narrative_metadata=s.narrative_metadata,
        semantic_lineage=s.semantic_lineage,
        utac_state=s.utac_state,
    )
    result = validate_sigillin(broken)
    assert result.valid is False


# ---------------------------------------------------------------------------
# Replay accuracy
# ---------------------------------------------------------------------------

def test_replay_reconstruct_exact_state() -> None:
    """Replay rekonstruiert exakten Zustand aus serialisierter Form (BENCHMARK: replay_accuracy)."""
    original = make_sigil()
    raw = serialize_sigillin(original)
    replayed = deserialize_sigillin(raw)

    assert replayed.q4_state.id == 11
    assert replayed.q4_state.binary == "1011"
    assert abs(replayed.crep_values.C - 0.82) < 1e-9
    assert abs(replayed.crep_values.Gamma - 0.736) < 1e-9
    assert abs(replayed.utac_state.H - 0.73) < 1e-9
    assert replayed.symbolic_identity == "heimkehr"

def test_replay_narrative_preserved() -> None:
    s = make_sigil(context="replay-ctx", intention="replay-intent", cycle=7)
    restored = deserialize_sigillin(serialize_sigillin(s))
    assert restored.narrative_metadata.context == "replay-ctx"
    assert restored.narrative_metadata.cycle == 7


# ---------------------------------------------------------------------------
# Lineage traversal
# ---------------------------------------------------------------------------

def test_link_sigillins_adds_parent_id() -> None:
    """child.semantic_lineage enthält parent.id (BENCHMARK: lineage_traversal)."""
    parent = make_sigil(symbolic_identity="wurzel")
    child = link_sigillins(parent, dict(
        q4_state=Q4StateData(C=1, R=1, E=1, P=1),
        crep=CREP,
        symbolic_identity="ast",
        timestamp=FIXED_TS,
    ))
    assert parent.id in child.semantic_lineage

def test_lineage_chain_traversal() -> None:
    """Vollständige Lineage-Kette traversierbar (BENCHMARK: lineage_traversal)."""
    root = make_sigil(symbolic_identity="root", timestamp=FIXED_TS)
    mid = link_sigillins(root, dict(
        q4_state=Q4,
        crep=CREP,
        symbolic_identity="mid",
        timestamp="2026-04-20T00:00:00+00:00",
    ))
    leaf = link_sigillins(mid, dict(
        q4_state=Q4,
        crep=CREP,
        symbolic_identity="leaf",
        timestamp="2026-04-21T00:00:00+00:00",
    ))

    assert root.id in leaf.semantic_lineage
    assert mid.id in leaf.semantic_lineage
    assert len(leaf.semantic_lineage) == 2

def test_link_sigillins_id_differs_from_parent() -> None:
    parent = make_sigil(symbolic_identity="elter")
    child = link_sigillins(parent, dict(
        q4_state=Q4,
        crep=CREP,
        symbolic_identity="kind",
        timestamp="2026-04-22T00:00:00+00:00",
    ))
    assert child.id != parent.id

def test_empty_lineage_for_root() -> None:
    root = make_sigil()
    assert root.semantic_lineage == []

def test_lineage_serializes_correctly() -> None:
    parent = make_sigil(symbolic_identity="p", timestamp=FIXED_TS)
    child = link_sigillins(parent, dict(
        q4_state=Q4,
        crep=CREP,
        symbolic_identity="c",
        timestamp="2026-04-23T00:00:00+00:00",
    ))
    raw = serialize_sigillin(child)
    restored = deserialize_sigillin(raw)
    assert parent.id in restored.semantic_lineage


# ---------------------------------------------------------------------------
# Schema completeness
# ---------------------------------------------------------------------------

def test_all_required_fields_present() -> None:
    s = make_sigil()
    d = s.to_dict()
    for key in ("id", "version", "timestamp", "symbolic_identity", "q4_state",
                "crep_values", "narrative_metadata", "semantic_lineage", "utac_state"):
        assert key in d, f"Pflichtfeld fehlt: {key!r}"

def test_q4_state_dict_has_binary() -> None:
    s = make_sigil()
    assert "binary" in s.to_dict()["q4_state"]

def test_crep_gamma_present() -> None:
    s = make_sigil()
    assert "Gamma" in s.to_dict()["crep_values"]
