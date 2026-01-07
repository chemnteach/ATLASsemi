# ATLASsemi Claude Rules

This directory contains behavioral rules specific to ATLASsemi development.

## What Goes Here

Project-specific rules that override or extend global Claude Code rules:

- **Security tier enforcement rules** (already handled by `tier_enforcer.py`)
- **Agent development patterns**
- **8D methodology guidelines**
- **Cost control rules**
- **Testing requirements**

## Global Rules

Most rules are inherited from the global `~/.claude/rules/` installation:

- `agent-orchestration.md` - When to use agents vs direct work
- `continuity.md` - Ledger management, multi-phase tracking
- `git-commits.md` - Use /commit skill, reasoning capture
- `hooks.md` - Shell wrapper → TypeScript pattern
- `observe-before-editing.md` - Check outputs before fixing
- And others...

## Creating New Rules

Add project-specific rules as needed:

```markdown
# Rule Name

## Pattern

[Describe the pattern]

## DO

- [Good practices]

## DON'T

- [Anti-patterns]

## Examples

[Show concrete examples]
```

Rules are automatically loaded by Claude Code.
