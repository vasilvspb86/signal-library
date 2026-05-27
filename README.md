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

## Getting feedback on a signal you authored

The pre-commit hook runs **two stages** on every push:

1. **Hard validation** (`validate_signals.cli`) — blocks the push if any of the 12 MUST fields are blank, the taxonomy is violated, body sections are missing, or URLs are malformed. You'll see `FAIL <file>: <reason>` and the push aborts.
2. **Soft lint** (`validate_signals.lint`) — non-blocking quality warnings. Catches things like: `name` field equals the slug, H1 doesn't match `name`, Bridge Map has empty `[[]]` placeholders, MAY fields set to empty string, anti-hype too short or too long (pasted abstract), `human_task` missing `?`, template placeholders still in body. Shows as `WARN <file>: <reason>` and the push proceeds.

**Run either stage manually before pushing:**

```bash
# Hard validation only — same as the pre-commit hook's stage 1
python -m validate_signals.cli signals/active/your-new-signal.md --taxonomy signals/_taxonomy.yml

# Soft lint only — same as the pre-commit hook's stage 2
python -m validate_signals.lint signals/active/your-new-signal.md

# Lint the entire library at once
python -m validate_signals.lint signals/active/*.md
```

For ongoing quality monitoring in Obsidian, open `_dashboards/needs-attention.md` — it's a live Dataview view of any active signal with blank MUSTs.

## Folder layout

- `signals/active/` — library-verified signals (each is one `.md` file)
- `signals/_inbox/` — drafts awaiting triage (`_manual/`, `_ai-candidates/`, `_telegram/`)
- `signals/_retired/` — preserved retired signals
- `signals/_taxonomy.yml` — controlled vocabulary for `domain` + Compas segments
- `templates/` — Templater scaffolds
- `_dashboards/` — Dataview-powered Obsidian dashboards
- `tools/` — Python validation hook + pipeline-facing library module
