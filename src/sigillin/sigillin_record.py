"""SigillinRecord — deterministisches SHA256-Schema mit Lineage-Support.

Sigillin ist das "Gedächtnis" des Systems: semantische Zustandsanker mit
deterministischen IDs und vollständiger Replay-Fähigkeit.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Q4State (lokal — wird künftig durch genesis-q4-core ersetzt)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Q4StateData:
    """4-Bit Zustand im GenesisAeon Q4-Zustandsraum.

    INVARIANTE: 16 Zustände = 4 Bit. Nicht 16 Bit.
    """
    C: int  # 0 oder 1 (Kohärenz-Flag)
    R: int  # 0 oder 1 (Resonanz-Flag)
    E: int  # 0 oder 1 (Emergenz-Flag)
    P: int  # 0 oder 1 (Poetik-Flag)

    def __post_init__(self) -> None:
        for name, val in [("C", self.C), ("R", self.R), ("E", self.E), ("P", self.P)]:
            if val not in (0, 1):
                raise ValueError(f"Q4StateData.{name} must be 0 or 1, got {val!r}")

    @property
    def id(self) -> int:
        return 8 * self.C + 4 * self.R + 2 * self.E + self.P

    @property
    def binary(self) -> str:
        return f"{self.id:04b}"

    def to_dict(self) -> dict[str, Any]:
        return {"C": self.C, "R": self.R, "E": self.E, "P": self.P,
                "id": self.id, "binary": self.binary}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Q4StateData:
        return cls(C=int(d["C"]), R=int(d["R"]), E=int(d["E"]), P=int(d["P"]))


# ---------------------------------------------------------------------------
# CREPValues
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CREPValues:
    """Kontinuierliche CREP-Float-Werte inkl. Gamma."""
    C: float
    R: float
    E: float
    P: float
    Gamma: float

    def to_dict(self) -> dict[str, float]:
        return {"C": self.C, "R": self.R, "E": self.E, "P": self.P, "Gamma": self.Gamma}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CREPValues:
        return cls(C=float(d["C"]), R=float(d["R"]), E=float(d["E"]),
                   P=float(d["P"]), Gamma=float(d["Gamma"]))


# ---------------------------------------------------------------------------
# UTACState
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class UTACState:
    """UTAC-Parameter (H, H_star, K_eff)."""
    H: float
    H_star: float
    K_eff: float

    def to_dict(self) -> dict[str, float]:
        return {"H": self.H, "H_star": self.H_star, "K_eff": self.K_eff}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> UTACState:
        return cls(H=float(d["H"]), H_star=float(d["H_star"]), K_eff=float(d["K_eff"]))


# ---------------------------------------------------------------------------
# NarrativeMetadata
# ---------------------------------------------------------------------------

@dataclass
class NarrativeMetadata:
    """Narrativer Kontext eines Sigillin-Records."""
    context: str = ""
    intention: str = ""
    cycle: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"context": self.context, "intention": self.intention, "cycle": self.cycle}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> NarrativeMetadata:
        return cls(context=str(d.get("context", "")),
                   intention=str(d.get("intention", "")),
                   cycle=int(d.get("cycle", 0)))


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


# ---------------------------------------------------------------------------
# SigillinRecord
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ("id", "version", "timestamp", "symbolic_identity",
                   "q4_state", "crep_values", "narrative_metadata",
                   "semantic_lineage", "utac_state")

SIGILLIN_VERSION = "1.0.0"


@dataclass
class SigillinRecord:
    """Semantischer Zustandsanker mit deterministischer SHA256-ID und Lineage.

    Schema:
      id:                 "sig_<sha256[:16]>" — deterministisch aus Inhalt
      version:            "1.0.0"
      timestamp:          ISO-8601 UTC
      symbolic_identity:  Bezeichner (z.B. "heimkehr")
      q4_state:           Q4StateData
      crep_values:        CREPValues
      narrative_metadata: NarrativeMetadata
      semantic_lineage:   list[str] — IDs der Vorgänger-Sigillins
      utac_state:         UTACState
    """
    id: str
    version: str
    timestamp: str
    symbolic_identity: str
    q4_state: Q4StateData
    crep_values: CREPValues
    narrative_metadata: NarrativeMetadata
    semantic_lineage: list[str]
    utac_state: UTACState

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "timestamp": self.timestamp,
            "symbolic_identity": self.symbolic_identity,
            "q4_state": self.q4_state.to_dict(),
            "crep_values": self.crep_values.to_dict(),
            "narrative_metadata": self.narrative_metadata.to_dict(),
            "semantic_lineage": list(self.semantic_lineage),
            "utac_state": self.utac_state.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SigillinRecord:
        return cls(
            id=str(d["id"]),
            version=str(d["version"]),
            timestamp=str(d["timestamp"]),
            symbolic_identity=str(d["symbolic_identity"]),
            q4_state=Q4StateData.from_dict(d["q4_state"]),
            crep_values=CREPValues.from_dict(d["crep_values"]),
            narrative_metadata=NarrativeMetadata.from_dict(d["narrative_metadata"]),
            semantic_lineage=list(d["semantic_lineage"]),
            utac_state=UTACState.from_dict(d["utac_state"]),
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_sigillin_id(content: dict[str, Any]) -> str:
    """SHA256-Hash des normalisierten Inhalts — deterministisch.

    Der content-dict wird ohne das 'id'-Feld gehasht (da die ID selbst
    aus dem Inhalt berechnet wird). Reihenfolge-unabhängig via sort_keys.
    """
    content_without_id = {k: v for k, v in content.items() if k != "id"}
    canonical = json.dumps(content_without_id, sort_keys=True, ensure_ascii=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sig_{digest[:16]}"


def create_sigillin(
    q4_state: Q4StateData,
    crep: CREPValues,
    symbolic_identity: str,
    context: str = "",
    intention: str = "",
    cycle: int = 0,
    utac: UTACState | None = None,
    lineage: list[str] | None = None,
    timestamp: str | None = None,
) -> SigillinRecord:
    """Erstellt einen neuen SigillinRecord mit deterministischer SHA256-ID."""
    ts = timestamp or datetime.now(timezone.utc).isoformat()
    narrative = NarrativeMetadata(context=context, intention=intention, cycle=cycle)
    utac_state = utac or UTACState(H=0.0, H_star=0.0, K_eff=0.0)
    parent_ids = list(lineage) if lineage else []

    content: dict[str, Any] = {
        "version": SIGILLIN_VERSION,
        "timestamp": ts,
        "symbolic_identity": symbolic_identity,
        "q4_state": q4_state.to_dict(),
        "crep_values": crep.to_dict(),
        "narrative_metadata": narrative.to_dict(),
        "semantic_lineage": parent_ids,
        "utac_state": utac_state.to_dict(),
    }
    record_id = compute_sigillin_id(content)
    return SigillinRecord(
        id=record_id,
        version=SIGILLIN_VERSION,
        timestamp=ts,
        symbolic_identity=symbolic_identity,
        q4_state=q4_state,
        crep_values=crep,
        narrative_metadata=narrative,
        semantic_lineage=parent_ids,
        utac_state=utac_state,
    )


def serialize_sigillin(sigillin: SigillinRecord, fmt: str = "json") -> str:
    """Serialisiert einen SigillinRecord als JSON oder YAML."""
    d = sigillin.to_dict()
    if fmt == "yaml":
        return yaml.dump(d, allow_unicode=True, sort_keys=True)
    return json.dumps(d, ensure_ascii=False, indent=2)


def deserialize_sigillin(data: str, fmt: str = "json") -> SigillinRecord:
    """Deserialisiert einen SigillinRecord aus JSON oder YAML."""
    if fmt == "yaml":
        d = yaml.safe_load(data)
    else:
        d = json.loads(data)
    return SigillinRecord.from_dict(d)


def validate_sigillin(sigillin: SigillinRecord) -> ValidationResult:
    """Prüft das SigillinRecord-Schema auf Vollständigkeit und Konsistenz."""
    errors: list[str] = []
    d = sigillin.to_dict()

    for f in REQUIRED_FIELDS:
        if f not in d or d[f] is None:
            errors.append(f"Pflichtfeld fehlt: {f!r}")

    if not sigillin.id.startswith("sig_"):
        errors.append(f"ID hat falsches Präfix: {sigillin.id!r}")

    recomputed = compute_sigillin_id(d)
    if sigillin.id != recomputed:
        errors.append(f"ID-Mismatch: gespeichert={sigillin.id!r}, erwartet={recomputed!r}")

    if sigillin.version != SIGILLIN_VERSION:
        errors.append(f"Unbekannte Version: {sigillin.version!r}")

    for flag, name in [(sigillin.q4_state.C, "C"), (sigillin.q4_state.R, "R"),
                       (sigillin.q4_state.E, "E"), (sigillin.q4_state.P, "P")]:
        if flag not in (0, 1):
            errors.append(f"Q4State.{name} muss 0 oder 1 sein")

    return ValidationResult(valid=len(errors) == 0, errors=errors)


def link_sigillins(parent: SigillinRecord, child_params: dict[str, Any]) -> SigillinRecord:
    """Erstellt einen neuen SigillinRecord der den parent in seiner Lineage referenziert.

    child_params: Keyword-Args für create_sigillin (ohne 'lineage').
    Die Lineage des child enthält alle IDs des parent + parent.id selbst.
    """
    new_lineage = list(parent.semantic_lineage) + [parent.id]
    return create_sigillin(
        lineage=new_lineage,
        **child_params,
    )
