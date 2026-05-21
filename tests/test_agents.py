"""Tests for multi-agent command format adaptation."""

from adm_cli.agents import adapt_command, command_filename

SAMPLE_COMMAND = """---
description: Trace data lifecycle — Phase 1 of ADM.
handoffs:
  - label: Run Inventory
    agent: adm.inventory
    prompt: Catalogue every column
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

This is the command body.
"""


class TestCommandFilename:
    def test_claude_dot_md(self):
        assert command_filename("lineage", "claude") == "adm.lineage.md"

    def test_gemini_dot_toml(self):
        assert command_filename("lineage", "gemini") == "adm.lineage.toml"

    def test_copilot_hyphen_md(self):
        assert command_filename("lineage", "copilot") == "adm-lineage.md"

    def test_q_hyphen_toml(self):
        assert command_filename("lineage", "q") == "adm-lineage.toml"

    def test_windsurf_hyphen_md(self):
        assert command_filename("lineage", "windsurf") == "adm-lineage.md"

    def test_cursor_dot_md(self):
        assert command_filename("lineage", "cursor") == "adm.lineage.md"


class TestAdaptCommand:
    def test_claude_preserves_original(self):
        result = adapt_command(SAMPLE_COMMAND, "claude")
        assert "handoffs:" in result
        assert "$ARGUMENTS" in result

    def test_gemini_converts_to_toml(self):
        result = adapt_command(SAMPLE_COMMAND, "gemini")
        assert result.startswith('description = "')
        assert 'prompt = """' in result
        assert "{{args}}" in result
        assert "$ARGUMENTS" not in result
        assert "handoffs" not in result

    def test_q_converts_to_toml(self):
        result = adapt_command(SAMPLE_COMMAND, "q")
        assert 'description = "' in result
        assert "{{args}}" in result

    def test_copilot_strips_handoffs(self):
        result = adapt_command(SAMPLE_COMMAND, "copilot")
        assert "handoffs:" not in result
        assert "agent: adm.inventory" not in result
        assert "$ARGUMENTS" in result
        assert "## Outline" in result

    def test_windsurf_strips_handoffs(self):
        result = adapt_command(SAMPLE_COMMAND, "windsurf")
        assert "handoffs:" not in result
        assert "## Outline" in result

    def test_cursor_strips_handoffs(self):
        result = adapt_command(SAMPLE_COMMAND, "cursor")
        assert "handoffs:" not in result
        assert "description:" in result
