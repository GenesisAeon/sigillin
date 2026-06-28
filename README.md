# sigillin

**The poetic-symbolic interface layer** – self-referential sigils that bind fieldtheory,
cosmic moments and entropy governance into living resonance.

[![CI](https://github.com/GenesisAeon/sigillin/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/sigillin/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: GPLv3+ / CC BY 4.0](https://img.shields.io/badge/License-GPLv3%2B%20%2F%20CC%20BY%204.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/sigillin)](https://pypi.org/project/sigillin/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19029975.svg)](https://doi.org/10.5281/zenodo.19029975)

---

## Installation

```bash
pip install sigillin
# or
uv add sigillin

# Full GenesisAeon stack integration
pip install "sigillin[stack]"
```

## Usage

```bash
# Validate a sigil against the CREP schema
sig validate codex-sigil.yaml

# Render MandalaMap resonance spectrum
sig render cosmic-web.yaml

# Inspect sigil fields
sig inspect codex-sigil.yaml

# Create a self-referential provider bridge
sig bridge openai
```

## Sigil format (trilayer: YAML / JSON / Markdown)

Sigillin accepts three source formats:

```yaml
# codex-sigil.yaml
coherence: 0.97
resonance: 0.88
emergence: 0.92
poetics: "The first sigil – carrier of the primal pattern."
```

```json
{ "coherence": 0.97, "resonance": 0.88, "emergence": 0.92, "poetics": "..." }
```

```markdown
---
coherence: 0.97
resonance: 0.88
emergence: 0.92
poetics: "The first sigil – carrier of the primal pattern."
---
# Codex Prime

Full narrative description here.
```

## CREP validation

Every sigil is validated against four pillars:

| Key | Meaning |
|---|---|
| `coherence` | Internal self-consistency |
| `resonance` | Harmonic alignment with the field |
| `emergence` | Capacity for novel pattern generation |
| `poetics` | Narrative / symbolic intent |

```python
from sigillin import Sigil

sigil = Sigil("codex-sigil.yaml")
sigil.validate_crep()   # True / False
sigil.assert_crep()     # raises SigilValidationError if invalid
```

## MandalaMap resonance

```python
spectrum = sigil.render_mandala(depth=0.618)  # φ-scaled resonance array
print(f"Peak: {spectrum.max():.4f}")
```

## Stack integration

With `pip install sigillin[stack]`, sigillin binds directly to the full GenesisAeon stack:

```python
sigil.bind_to_field()   # returns Lagrangian string from fieldtheory
```

```python
from sigillin.entropy_table_bridge import export_to_entropy_table
export_to_entropy_table("codex-sigil.yaml")
```

## Python API

```python
from sigillin import Sigil

sigil = Sigil("codex-sigil.yaml")
print(sigil["coherence"])          # 0.97
print(sigil.get("tags", []))       # []
print(repr(sigil))                 # Sigil(path=..., crep_valid=True)
```

## Role in the GenesisAeon Ecosystem

`sigillin` (P-SIGIL) is the symbolic interface layer of the GenesisAeon
stack: it provides the semantic state anchors and trilayer sigil format
that bind `fieldtheory`, `cosmic-moment`, `medium-modulation`, and
`entropy-governance` into a shared, validatable representation.

## License

This repository is dual-licensed:

- **Source code** — [GNU General Public License v3.0 or later](LICENSE-CODE) (GPL-3.0-or-later)
- **Documentation** (this README, `docs/`, and other written content) —
  [Creative Commons Attribution 4.0 International](LICENSE-DOCS) (CC BY 4.0)

See [LICENSE](LICENSE) for details.

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19029975.svg)](https://doi.org/10.5281/zenodo.19029975)

If you use `sigillin` in research, please cite via the Zenodo DOI above.
A new DOI version is minted automatically on each GitHub Release once
Zenodo-GitHub integration is enabled for this repo.

---

Built with [uv](https://docs.astral.sh/uv/) · [Typer](https://typer.tiangolo.com/) ·
[Rich](https://rich.readthedocs.io/) · [NumPy](https://numpy.org/)
