# Architecture Guidelines

## CLI Architecture

- **Typer** for command definitions, **Rich** for formatted output
- Each command gets its own module: `init.py`, `check.py`, `status.py`, `gates.py`
- `__init__.py` wires commands into the typer app — keep it thin
- Commands accept a `project_dir: Path | None` parameter for testability

## Module Pattern

Every command module follows this pattern:
1. A `run_<command>()` function that does the work
2. The typer command in `__init__.py` calls it
3. No global state — pass project_dir explicitly

## State Management

- Single source of truth: `.adm/project.json`
- Load via `schema.load_state()`, save via `schema.save_state()`
- All state modifications are atomic (load → modify → save)
- Never modify state in read-only commands (check, status)

## Templates

- Templates bundled in `src/adm_cli/templates/` (package data)
- Accessed via `importlib.resources`
- YAML frontmatter defines machine-readable metadata
- Markdown body is for humans and AI agents

## Dependencies

- Keep dependencies minimal: typer, rich, pydantic, pyyaml, platformdirs
- Use stdlib where possible (subprocess, importlib, pathlib)
- No heavy frameworks — this is a CLI tool, not a web service

## File Layout

```
src/adm_cli/
├── __init__.py          # App definition + command wiring
├── schema.py            # Pydantic state models + load/save
├── init.py              # adm init command
├── check.py             # adm check command
├── status.py            # adm status command
├── gates.py             # Phase gate enforcement
└── templates/           # Bundled templates (package data)
    ├── commands/        # AI agent command files
    └── phases/          # Phase artefact templates
```
