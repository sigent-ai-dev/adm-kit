# Code Standards

## General Principles

- Write clear, self-documenting code
- Keep functions small and focused (max 30 lines)
- Use meaningful variable and function names
- Handle errors gracefully with specific exceptions
- Write testable code — prefer pure functions

## Complexity Targets

- **Cyclomatic Complexity**: Keep functions below 10 (aim for ≤5)
- **Function Length**: Maximum 30 lines per function
- **File Length**: Maximum 300 lines per file (split if larger)
- **Nesting Depth**: Maximum 3 levels

## Python-Specific

### Code Organization
```python
# 1. Standard library imports
from __future__ import annotations
from pathlib import Path

# 2. Third-party imports
from pydantic import BaseModel
from rich.console import Console

# 3. Local imports
from .schema import ProjectState
```

### Naming
- **Constants**: `UPPER_SNAKE_CASE`
- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Private**: Prefix with `_`

### Error Handling
- Early returns for validation
- Specific exceptions (not bare `Exception`)
- Include context in error messages
- Use `SystemExit(1)` for CLI errors, not `sys.exit()`

## Testing (pytest)

- Use `tmp_path` fixtures for filesystem tests
- Use class grouping for related tests
- Use `@pytest.mark.parametrize` to eliminate test duplication
- Test error paths, not just happy paths
- Minimum 70% coverage
