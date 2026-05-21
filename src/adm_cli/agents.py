"""Multi-agent command format adaptation."""

from __future__ import annotations

COMMAND_PREFIX = "adm"

AGENT_FORMAT: dict[str, str] = {
    "claude": "markdown",
    "gemini": "toml",
    "copilot": "markdown",
    "cursor": "markdown",
    "q": "toml",
    "windsurf": "markdown",
}

AGENT_SEPARATOR: dict[str, str] = {
    "claude": ".",
    "gemini": ".",
    "copilot": "-",
    "cursor": ".",
    "q": "-",
    "windsurf": "-",
}


def _extract_frontmatter(content: str) -> tuple[str, str]:
    """Split markdown into frontmatter and body."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", content
    return parts[1].strip(), parts[2].strip()


def _convert_to_toml(content: str) -> str:
    """Convert markdown command file to TOML format for Gemini/Q."""
    frontmatter, body = _extract_frontmatter(content)

    description = ""
    for line in frontmatter.split("\n"):
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    body = body.replace("$ARGUMENTS", "{{args}}")

    return f'description = "{description}"\n\nprompt = """\n{body}\n"""\n'


def _strip_claude_fields(content: str) -> str:
    """Remove Claude-specific frontmatter fields (handoffs, scripts)."""
    frontmatter, body = _extract_frontmatter(content)

    cleaned_lines = []
    skip_block = False
    for line in frontmatter.split("\n"):
        if line.startswith("handoffs:") or line.startswith("scripts:") or line.startswith("agent_scripts:"):
            skip_block = True
            continue
        if skip_block and (line.startswith("  ") or line.startswith("\t")):
            continue
        skip_block = False
        cleaned_lines.append(line)

    cleaned_fm = "\n".join(cleaned_lines).strip()
    if cleaned_fm:
        return f"---\n{cleaned_fm}\n---\n\n{body}\n"
    return f"---\ndescription: \"\"\n---\n\n{body}\n"


def adapt_command(content: str, agent: str) -> str:
    """Adapt a command file from source (Claude markdown) to target agent format."""
    fmt = AGENT_FORMAT.get(agent, "markdown")

    if fmt == "toml":
        return _convert_to_toml(content)

    if agent != "claude":
        return _strip_claude_fields(content)

    return content


def command_filename(base_name: str, agent: str) -> str:
    """Generate the correct filename for a command installed to an agent.

    base_name: stem without extension (e.g., "lineage", "clarify")
    """
    sep = AGENT_SEPARATOR.get(agent, ".")
    ext = "toml" if AGENT_FORMAT.get(agent) == "toml" else "md"
    return f"{COMMAND_PREFIX}{sep}{base_name}.{ext}"
