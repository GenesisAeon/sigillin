# Contributing

Thanks for your interest in contributing to `sigillin`!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`.
3. Install in editable mode with dev dependencies: `pip install -e ".[dev]"`.
4. Run the test suite: `pytest`.

## Code style

- Format and lint with `ruff` (`ruff check src tests`).
- Type-check with `mypy src`.
- Keep functions documented with docstrings.

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Licensing of contributions

By contributing source code you agree it is licensed under
GPL-3.0-or-later, and by contributing documentation you agree it is
licensed under CC BY 4.0, consistent with this repository's dual license
(see `LICENSE`, `LICENSE-CODE`, `LICENSE-DOCS`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.
