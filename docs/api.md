# API Reference

## sigillin.core.Sigil

```python
class Sigil(filepath: Path | str)
```

Self-referential poetic-symbolic attractor. Loads a sigil from YAML, JSON, or
Markdown front-matter (trilayer).

### Methods

| Method | Description |
|---|---|
| `validate_crep() -> bool` | Returns `True` if all four CREP keys are present |
| `assert_crep() -> None` | Raises `SigilValidationError` if CREP keys are missing |
| `render_mandala(depth=0.618) -> np.ndarray` | Returns φ-scaled resonance spectrum (shape: 100) |
| `bind_to_field() -> str` | Binds to fieldtheory Lagrangian (requires `[stack]`) |
| `get(key, default=None)` | Dict-style attribute access with default |

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `path` | `Path` | Source file path |
| `data` | `dict[str, Any]` | Parsed sigil data |

---

## sigillin.core.SigilValidationError

Raised by `assert_crep()` when required CREP keys are missing.

---

## sigillin.entropy_table_bridge

```python
sigil_to_entropy_record(sigil: Sigil) -> dict[str, Any]
export_to_entropy_table(path: Path | str) -> None
```

Exports sigil data to entropy-table format. Requires `sigillin[stack]`.
