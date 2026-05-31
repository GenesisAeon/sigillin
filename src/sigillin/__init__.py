"""sigillin â€“ the poetic-symbolic interface layer of the GenesisAeon stack."""

__version__ = "0.4.0"
__all__ = [
    "Sigil",
    "SigillinRecord",
    "Q4StateData",
    "CREPValues",
    "UTACState",
    "NarrativeMetadata",
    "ValidationResult",
    "create_sigillin",
    "serialize_sigillin",
    "deserialize_sigillin",
    "validate_sigillin",
    "link_sigillins",
    "compute_sigillin_id",
]

from .core import Sigil
from .sigillin_record import (
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

