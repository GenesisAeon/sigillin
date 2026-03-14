"""entropy-table bridge – export sigillin data into entropy-table format.

Requires ``sigillin[stack]`` (``entropy-table>=1.0.1``).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import Sigil


def sigil_to_entropy_record(sigil: Sigil) -> dict[str, Any]:
    """Convert a :class:`Sigil` to a flat entropy-table record.

    The record schema mirrors the trilayer CREP structure so that it can be
    ingested directly by ``entropy_table.register()``.
    """
    spectrum = sigil.render_mandala()
    return {
        "name": sigil.path.stem,
        "coherence": sigil.get("coherence", 0.0),
        "resonance": sigil.get("resonance", 0.0),
        "emergence": sigil.get("emergence", 0.0),
        "poetics": sigil.get("poetics", ""),
        "mandala_peak": float(spectrum.max()),
        "mandala_mean": float(spectrum.mean()),
        "source_path": str(sigil.path),
        "crep_valid": sigil.validate_crep(),
    }


def export_to_entropy_table(path: Path | str) -> None:
    """Load a sigil and register it with entropy-table (requires ``[stack]``).

    Raises :class:`ImportError` with a helpful message when the ``[stack]``
    extra is not installed.
    """
    try:
        from entropy_table import register  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "entropy-table is not installed. "
            "Install it with: pip install sigillin[stack]"
        ) from exc

    sigil = Sigil(path)
    record = sigil_to_entropy_record(sigil)
    register(record)
