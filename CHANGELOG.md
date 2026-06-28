# Changelog

## [1.0.0] - 2026

### Added
- Standardized release tooling: `.zenodo.json`, `RELEASE_GUIDE.md`,
  `CONTRIBUTING.md`, issue/PR templates.

### Changed
- Project metadata (`pyproject.toml`) normalized: version bumped to
  1.0.0, and GenesisAeon-ecosystem dependency pins updated to the
  released floor versions (`entropy-table>=2.0.0`,
  `implosive-genesis>=1.0.0`, `fieldtheory>=1.0.0`,
  `cosmic-moment>=1.0.0`, `medium-modulation>=1.0.0`,
  `entropy-governance>=1.0.0`).
- Relicensed: source code is now GPL-3.0-or-later, documentation is now
  CC BY 4.0 (previously MIT). See `LICENSE`, `LICENSE-CODE`, and
  `LICENSE-DOCS`.

## v0.1.0 (2026-03-15)

- Initial release: trilayer Sigil loader (YAML/JSON/Markdown) with CREP validation
- CLI `sig validate` + `sig render` + `sig bridge`
- MandalaMap resonance spectrum + field-theory binding
- 28/28 tests, 84 % coverage, ruff + mkdocs clean
- `[stack]` extra für GenesisAeon-Stack
- DOI: [10.5281/zenodo.19029975](https://doi.org/10.5281/zenodo.19029975)
