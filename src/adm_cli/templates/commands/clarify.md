---
description: Resolve open clarification questions (CLR-NNN) raised during any ADM phase.
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.clarify` is a utility command that can run at ANY phase. It lists open clarification questions (CLR-NNN), helps resolve them with analyst input, and persists resolutions so they survive phase re-runs.

### Gate Check

- `.adm/project.json` must exist
- At least one domain must be initialised

No phase gate — this command is always available.

### Execution Flow

1. **Identify the domain** from user input or state (if single domain, use it; if multiple, ask).

2. **Gather open questions** from all phase artefacts:
   - Scan `artefacts/<domain>/*/` for files containing `CLR-NNN` entries with status "open"
   - Load resolutions from `.adm/project.json` → `domains.<domain>.resolutions`
   - Build a combined list: all CLR-NNN across all phases with current status

3. **Display open questions**:
   ```markdown
   ## Open Clarifications: <domain>

   | ID | Phase | Question | Impact |
   |----|-------|----------|--------|
   | CLR-001 | 1-lineage | What does column X represent? | Blocks accurate typing in thesis |
   | CLR-003 | 2-inventory | Is null in column Y meaningful or missing data? | Affects nullability invariant |

   **Total**: N open / M resolved
   ```

4. **Resolution flow** (interactive):
   - If user specified a CLR-NNN ID in arguments → resolve that one
   - Otherwise → present the list and ask which to resolve
   - For each resolution:
     a. Show the question and its context
     b. Ask the analyst for the answer
     c. Record the resolution

5. **Persist resolution**:
   - Update `.adm/project.json` → `domains.<domain>.resolutions.CLR-NNN` = "resolved"
   - Update the source artefact where the question was raised (change status from "open" to "resolved", add the answer)
   - Write audit entry

6. **Report**:
   ```markdown
   ## Resolution Summary

   - Resolved this session: N
   - Remaining open: M
   - Ready for ratchet: [yes/no] (zero open CLR-NNN required)
   ```

7. **Recommend next step**:
   - If questions remain → suggest running `/adm.clarify` again or continuing the current phase
   - If all resolved → suggest advancing to the next phase

### Merge Behaviour

When a phase is re-run (e.g., lineage re-executed with new data):
- **Default (merge)**: Existing resolutions are preserved. New questions get new CLR-NNN IDs.
- **`--resolutions overwrite`**: Discard prior resolutions and re-raise all questions.
- **`--resolutions skip`**: Don't raise any new questions (use only existing resolutions).

## Guidelines

- NEVER discard a resolution without explicit analyst confirmation. Resolutions represent human decisions.
- CLR-NNN IDs are globally unique within a domain. Don't reuse IDs even if the original question is removed.
- Resolutions should be specific and actionable — "yes" or "no" is rarely sufficient. Capture the reasoning.
- If a resolution invalidates a prior phase artefact, note which phases need re-running.
- This command does NOT block any phase. It's advisory. Only `/adm.ratchet` enforces resolution completeness.
