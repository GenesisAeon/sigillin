# CLI Reference

## sig validate

```
sig validate PATH
```

Validate a sigil file against the CREP schema.

**Arguments:**
- `PATH` – path to sigil file (YAML, JSON, or Markdown with front-matter)

**Exit codes:** `0` = valid, `1` = invalid or file not found

---

## sig render

```
sig render PATH [--depth FLOAT]
```

Render the MandalaMap resonance spectrum for a sigil.

**Arguments:**
- `PATH` – path to sigil file

**Options:**
- `--depth` – fractal resonance depth (default: `0.618`, the golden ratio φ)

---

## sig inspect

```
sig inspect PATH
```

Inspect all fields of a sigil in a rich table, with CREP status.

---

## sig bridge

```
sig bridge [PROVIDER]
```

Create a self-referential provider bridge (default: `openai`).
