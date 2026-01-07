# Thoughts Directory

This directory contains **working memory** for Continuous Claude sessions.

**IMPORTANT:** These files should be committed to git (they're not in .gitignore).

## Structure

```
thoughts/
├── ledgers/               # Session state (survives /clear)
│   └── CONTINUITY_CLAUDE-*.md
│
└── shared/
    ├── handoffs/          # Between-session transfers
    │   └── task-*.md
    │
    └── plans/             # Implementation plans
        └── yyyy-mm-dd-*.md
```

## Ledgers

Ledgers preserve session state across `/clear` operations.

**When to create:**
- At session start (if complex multi-step work)
- Before `/clear` when context usage >70%
- When switching major tasks

**Format:**

```yaml
---
problem_mode: excursion|improvement|operations
security_tier: general_llm|confidential_fab|top_secret
api_routing: which endpoints to use
---

## Goal
[Success criteria]

## State
- Done: [✓] Completed items
- Now: [→] Current task
- Next: Upcoming work

## Key Decisions
[Choices made with rationale]

## Working Set
[Files, branch, commands]
```

## Handoffs

Handoffs transfer work between sessions or between people.

**When to create:**
- End of work session
- Handing off to another developer
- Major milestone completed

**Format:**

```markdown
# Handoff: [Task Name]

**Date:** 2026-01-07
**From:** Current session
**Status:** [In Progress / Blocked / Complete]

## Context
[What we were working on]

## What's Done
[Completed work]

## What's Next
[Immediate next steps]

## Key Files
[Files to review]

## Blockers
[Any issues]
```

## Plans

Implementation plans for complex features.

**When to create:**
- Multi-phase implementation
- Architecture changes
- New feature development

**Format:**

```markdown
# Plan: [Feature Name]

**Date:** 2026-01-07

## Phases

- [ ] Phase 1: [Description]
- [ ] Phase 2: [Description]
- [ ] Phase 3: [Description]

## Current Phase

[Details of current work]

## Dependencies

[What's required]
```

## Usage with Claude

```bash
# Create ledger
"Update ledger, I'm about to clear"

# Create handoff
"Create handoff, I'm done for today"

# Resume from handoff
"Resume from handoff"
```

## Why Commit These Files?

Unlike `.claude/cache/` (which is gitignored), the `thoughts/` directory should be committed because:

1. **Session continuity** - Other sessions can pick up where you left off
2. **Team visibility** - Others can see current work status
3. **Historical record** - Track evolution of complex implementations
4. **Context preservation** - Full fidelity across compaction/clear operations

**Exception:** Don't commit thoughts that contain proprietary fab data in Tier 2/3 sessions. In those cases, store thoughts outside the repo or use a separate private repo.
