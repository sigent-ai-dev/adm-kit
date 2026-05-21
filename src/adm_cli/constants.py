"""Shared constants for ADM CLI."""

PHASE_DIRS = [
    "1-lineage",
    "2-inventory",
    "3-invariants",
    "4-thesis",
    "5-validate",
    "6-contracts",
    "7-model",
]

PHASE_NAMES = {
    1: "Lineage",
    2: "Inventory",
    3: "Invariants",
    4: "Thesis",
    5: "Validate",
    6: "Ratchet",
    7: "Model",
}

AGENT_DIRS: dict[str, str] = {
    "claude": ".claude/commands",
    "gemini": ".gemini/commands",
    "copilot": ".github/agents",
    "cursor": ".cursor/commands",
    "q": ".amazonq/prompts",
    "windsurf": ".windsurf/workflows",
}
