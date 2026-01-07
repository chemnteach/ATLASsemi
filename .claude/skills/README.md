# ATLASsemi Custom Skills

This directory can contain custom Claude Code skills for common ATLASsemi operations.

## Available Global Skills

From Continuous Claude v2:

- `/commit` - Create git commits without Claude attribution
- `/continuity_ledger` - Save session state
- `/create_handoff` - Create between-session handoff
- `/resume_handoff` - Resume from handoff
- `/create_plan` - Create implementation plans
- And many others...

## Future ATLASsemi-Specific Skills

Potential custom skills for ATLASsemi workflows:

### 1. `/run-8d-workflow`
**Purpose:** Execute complete Phase 0-3 workflow on a problem

```bash
# Usage
/run-8d-workflow

# Prompts for:
# - Problem mode (excursion/improvement/operations)
# - Security tier
# - Narrative description
# Then runs all phases automatically
```

### 2. `/validate-8d`
**Purpose:** Validate a completed 8D report for completeness

```bash
# Usage
/validate-8d path/to/8d-report.md

# Checks:
# - All 8D phases addressed
# - Facts vs hypotheses separated
# - Confidence levels provided
# - Next steps defined
```

### 3. `/search-similar-cases`
**Purpose:** Search knowledge graph for similar historical cases

```bash
# Usage
/search-similar-cases "yield drop on litho tool"

# Returns:
# - Similar historical 8Ds
# - Common root causes
# - Successful fixes
```

### 4. `/tier-check`
**Purpose:** Verify current security tier before operations

```bash
# Usage
/tier-check

# Shows:
# - Current tier from ledger
# - Allowed tools
# - Blocked operations
```

## Creating Custom Skills

Skills are markdown files with:

```yaml
---
name: skill-name
description: Brief description
allowed-tools: [Bash, Read, Write]  # Optional restrictions
---

# Skill Instructions

[Detailed instructions for Claude]

## Examples

[Usage examples]
```

Register in `.claude/settings.json`:

```json
{
  "skills": {
    "skill-name": ".claude/skills/skill-name.md"
  }
}
```
