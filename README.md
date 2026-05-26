# Signal Library

The curated trend-signal library powering Signal Compass v0.

**See:** `../Trendwatching_materials/docs/superpowers/specs/2026-05-22-signal-library-design.md` for the full design spec.

## Quick start (curator)

1. Open this folder in Obsidian as a vault.
2. Install required plugins: **Templater**, **Dataview**, **Obsidian Git**.
3. Configure Obsidian Git: auto-pull every 2 min, auto-push every 5 min.
4. Subscribe to Obsidian Sync ($4/mo) and enable on this vault for mobile.
5. To add a signal: `Ctrl+N` → pick `signal-active.md` template → fill MUST fields → save to `signals/active/`.

## Quick start (engineer)

1. `cd tools/`
2. `python -m pip install -e ".[dev]"` (installs `validate_signals` + `signal_library`)
3. `pytest` to run all tests.
4. `python install_hook.py` to install the pre-commit validation hook.

## Folder layout

- `signals/active/` — library-verified signals (each is one `.md` file)
- `signals/_inbox/` — drafts awaiting triage (`_manual/`, `_ai-candidates/`, `_telegram/`)
- `signals/_retired/` — preserved retired signals
- `signals/_taxonomy.yml` — controlled vocabulary for `domain` + Compas segments
- `templates/` — Templater scaffolds
- `_dashboards/` — Dataview-powered Obsidian dashboards
- `tools/` — Python validation hook + pipeline-facing library module
