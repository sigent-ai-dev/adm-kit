# Testing Standards

## General Rules

- Minimum 70% line coverage
- Run tests before committing: `uv run --group dev pytest`
- Test error paths, not just happy paths
- Use `tmp_path` fixtures for all filesystem operations (never write to real dirs)

## Test Organization

```
tests/
├── test_schema.py       # State schema validation
├── test_init.py         # adm init command
├── test_check.py        # adm check command
├── test_status.py       # adm status command
├── test_gates.py        # Phase gate enforcement
└── conftest.py          # Shared fixtures (if needed)
```

## Patterns

### Use class grouping
```python
class TestValidProject:
    def test_exits_zero(self, tmp_path): ...
    def test_reports_no_errors(self, tmp_path): ...

class TestCorruptState:
    def test_reports_error(self, tmp_path): ...
```

### Use parametrize for similar cases
```python
@pytest.mark.parametrize("ai,expected_dir", [
    ("claude", ".claude/commands"),
    ("gemini", ".gemini/commands"),
    ("copilot", ".github/agents"),
])
def test_agent_dirs(self, tmp_path, ai, expected_dir): ...
```

### Test CLI via function, not subprocess
```python
# ✅ Good: Call the function directly
from adm_cli.init import run_init
run_init(domain="test", source=None, ai="claude", force=False, project_dir=tmp_path)

# ❌ Bad: Shell out to the CLI
subprocess.run(["adm", "init", "test"])
```

## What NOT to Test

- Rich output formatting (visual, not semantic)
- Third-party library internals (pydantic validation details)
- File content beyond existence checks (templates are tested once, not per-init)
