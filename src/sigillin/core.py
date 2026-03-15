"""SigilParser – trilayer YAML/JSON/Markdown loader with CREP validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from rich.console import Console

console = Console()

CREP_KEYS = ("coherence", "resonance", "emergence", "poetics")


class SigilValidationError(ValueError):
    """Raised when a sigil fails CREP validation."""


class Sigil:
    """Self-referential poetic-symbolic attractor.

    Supports three source formats (trilayer):
    - ``.yaml`` / ``.yml``  — structural definition (primary)
    - ``.json``             — machine-readable export
    - ``.md``               — narrative / free-form (parses YAML front-matter)
    """

    def __init__(self, filepath: Path | str) -> None:
        self.path = Path(filepath)
        self.data: dict[str, Any] = self._load_trilayer()

    # ------------------------------------------------------------------
    # Trilayer loading
    # ------------------------------------------------------------------

    def _load_trilayer(self) -> dict[str, Any]:
        suffix = self.path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            return self._load_yaml()
        if suffix == ".json":
            return self._load_json()
        if suffix == ".md":
            return self._load_markdown_frontmatter()
        # Fallback: try YAML first, then JSON
        try:
            return self._load_yaml()
        except Exception:
            return self._load_json()

    def _load_yaml(self) -> dict[str, Any]:
        with self.path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _load_json(self) -> dict[str, Any]:
        with self.path.open(encoding="utf-8") as f:
            return json.load(f)

    def _load_markdown_frontmatter(self) -> dict[str, Any]:
        """Extract YAML front-matter between ``---`` fences."""
        text = self.path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines and lines[0].strip() == "---":
            end = next(
                (i for i, ln in enumerate(lines[1:], 1) if ln.strip() == "---"),
                None,
            )
            if end is not None:
                front = "\n".join(lines[1:end])
                return yaml.safe_load(front) or {}
        return {}

    # ------------------------------------------------------------------
    # CREP validation
    # ------------------------------------------------------------------

    def validate_crep(self) -> bool:
        """Return True if all four CREP keys are present."""
        return all(k in self.data for k in CREP_KEYS)

    def assert_crep(self) -> None:
        """Raise :class:`SigilValidationError` if CREP keys are missing."""
        missing = [k for k in CREP_KEYS if k not in self.data]
        if missing:
            raise SigilValidationError(
                f"Sigil {self.path.name!r} is missing CREP keys: {missing}"
            )

    # ------------------------------------------------------------------
    # MandalaMap resonance
    # ------------------------------------------------------------------

    def render_mandala(self, depth: float = 0.618) -> np.ndarray:
        """Return a fractal resonance spectrum (placeholder MandalaMap binding).

        The golden-ratio depth parameter (φ ≈ 0.618) controls the oscillation
        frequency.  The returned array can be handed to fieldtheory for full
        Lagrangian integration when the ``[stack]`` extra is installed.
        """
        t = np.linspace(0, 10, 100)
        return np.sin(t * depth) * 1.618  # φ-scaled resonance spectrum

    # ------------------------------------------------------------------
    # Optional fieldtheory binding
    # ------------------------------------------------------------------

    def bind_to_field(self) -> str:
        """Bind this sigil to the fieldtheory Lagrangian (requires ``[stack]``)."""
        try:
            from fieldtheory.core import derive_lagrangian  # type: ignore[import]

            return str(derive_lagrangian())
        except ImportError:
            return "Lagrangian binding available with: pip install sigillin[stack]"

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Sigil(path={self.path!r}, crep_valid={self.validate_crep()})"

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
