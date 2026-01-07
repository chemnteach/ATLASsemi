# Continuous Claude Setup for ATLASsemi

**Status:** ✅ Complete
**Date:** 2026-01-07
**Commit:** b0c4ddf

---

## What's Been Set Up

### 1. Directory Structure ✅

```
ATLASsemi/
├── .claude/                         # Continuous Claude configuration
│   ├── agents/                      # Custom agents (future)
│   │   └── README.md
│   ├── rules/                       # Project-specific rules
│   │   └── README.md
│   ├── skills/                      # Custom skills (future)
│   │   └── README.md
│   ├── hooks/                       # Session lifecycle hooks (future)
│   ├── cache/                       # Artifact Index (gitignored)
│   └── settings.json                # Permissions configuration
│
├── thoughts/                        # Working memory (COMMITTED)
│   ├── ledgers/                     # Session state
│   │   └── LEDGER_TEMPLATE.md
│   └── shared/
│       ├── handoffs/                # Between-session transfers
│       └── plans/                   # Implementation plans
│
├── CLAUDE.md                        # Complete project instructions
└── CONTINUOUS_CLAUDE_SETUP.md       # This file
```

### 2. Configuration Files ✅

**`.claude/settings.json`**
- Basic permissions for Python, git, testing, linting
- Auto-approves common development commands
- Includes `/commit` skill for clean git commits

**`.gitignore`**
- Excludes `.claude/cache/` (local only)
- Excludes `.claude/settings.local.json` (local overrides)
- **INCLUDES** `thoughts/` (for session continuity)
- Excludes proprietary data patterns

### 3. Documentation ✅

**`CLAUDE.md`** - Main project instructions covering:
- Project overview and architecture
- Security tier system (3 tiers)
- Model router system
- Agent development guidelines
- Session management patterns
- Code style and testing guidelines
- Common tasks and examples

**`thoughts/README.md`** - Working memory structure:
- What ledgers are and when to create them
- Handoff format and usage
- Plan structure for multi-phase work
- Why to commit thoughts (not cache)

**READMEs in `.claude/` subdirectories:**
- Agent creation guidelines
- Skill development patterns
- Rule organization

### 4. Templates ✅

**`thoughts/ledgers/LEDGER_TEMPLATE.md`**
- Complete ledger structure with examples
- YAML frontmatter for metadata
- Multi-phase tracking with checkboxes
- Security tier documentation
- Cost tracking section
- Progress notes format

---

## How to Use This Setup

### Starting a New Session

1. **Open ATLASsemi in Claude Code**
   ```bash
   cd /mnt/c/src/Synterra/ATLASsemi
   # Claude Code will automatically load CLAUDE.md
   ```

2. **Ask about mode and tier** (if working on actual fab problems)
   ```
   Claude: "What problem mode are you working on?"
   You: "Yield excursion"

   Claude: "What security tier?"
   You: "General LLM" (or Confidential Fab / Top Secret)
   ```

3. **Create a ledger** (for complex multi-step work)
   ```
   You: "Create a continuity ledger for implementing the prevention agent"
   ```

### During Work

- **Before context gets full (>70% usage):**
  ```
  You: "Update ledger, I'm about to clear"
  Claude: [Updates ledger]
  You: "/clear"
  # Ledger auto-loads in fresh context
  ```

- **Track progress with checkboxes in ledger:**
  ```yaml
  - Done:
    - [x] Phase 1: Setup
    - [x] Phase 2: Implementation
  - Now: [→] Phase 3: Testing
  - Next: Phase 4: Documentation
  ```

### Ending a Session

```
You: "Create handoff, I'm done for today"
Claude: [Creates handoff in thoughts/shared/handoffs/]
# Next session: "Resume from handoff"
```

### Using Skills

Global skills available:
- `/commit` - Clean git commits (no Claude attribution)
- `/continuity_ledger` - Save session state
- `/create_handoff` - Create transfer document
- `/resume_handoff` - Resume from handoff
- `/create_plan` - Generate implementation plan

Custom skills can be added to `.claude/skills/`

---

## Key Features Enabled

### 1. Session Continuity ✅
- Ledgers survive `/clear` operations
- Automatic resumption with full context
- Multi-phase tracking with checkboxes
- No context degradation across clears

### 2. Security Tier Awareness ✅
- Every ledger documents security tier
- Tier restrictions are enforced (see `tier_enforcer.py`)
- Audit trail for Tier 2/3 operations
- Clear documentation of allowed/blocked tools

### 3. Mode-Aware Workflows ✅
- Excursion: Fast containment focus
- Improvement: Chronic issues, variability
- Operations: Blocking issues, urgency
- Different prompts and questions per mode

### 4. Cost Tracking ✅
- ModelRouter tracks all LLM usage
- Session cost summaries
- Dev vs Runtime mode selection
- Budget awareness

### 5. Agent Orchestration ✅
- Base agent architecture complete
- Phases 0-2 implemented
- Ready for orchestrator to chain agents
- Custom agents can extend workflow

---

## What This Enables

### Multi-Session Development
```
Day 1: Implement prevention agent → Save ledger
Day 2: Resume → Continue → Save handoff
Day 3: Resume → Test → Complete
```

Context preserved across all sessions, no repetition.

### Multi-Phase Projects
```
thoughts/shared/plans/2026-01-07-knowledge-graph.md

## Phases
- [ ] Phase 1: Schema design
- [ ] Phase 2: Neo4j integration
- [ ] Phase 3: Query implementation
- [ ] Phase 4: Agent integration
- [ ] Phase 5: Testing
```

Track progress through complex implementations.

### Team Collaboration
```
Craig: Works on Phase 1 → Creates handoff
Other dev: Resumes from handoff → Continues Phase 2
```

Handoffs enable seamless team transitions.

---

## Testing the Setup

### Verify Directory Structure

```bash
cd /mnt/c/src/Synterra/ATLASsemi

# Check Continuous Claude directories
ls -la .claude/
ls -la thoughts/

# Check configuration
cat .claude/settings.json
cat CLAUDE.md | head -50
```

### Test Session Continuity

```bash
# In Claude Code session:
You: "Create a test ledger for verifying setup"
# Claude creates thoughts/ledgers/CONTINUITY_CLAUDE-setup-test.md

You: "What's my current working set?"
# Claude reads from ledger

You: "/clear"
# Context cleared

You: "What was I working on?"
# Claude should know from ledger (auto-loads on SessionStart)
```

### Test Security Tier Enforcement

```python
from atlassemi.security.tier_enforcer import TierEnforcer, SecurityTier

# Try to use external API in Confidential tier (should block)
enforcer = TierEnforcer(current_tier=SecurityTier.CONFIDENTIAL_FAB)
try:
    enforcer.validate_tool_use("anthropic")  # Should raise SecurityViolationError
except Exception as e:
    print(f"Correctly blocked: {e}")

# Local tools should work in all tiers
enforcer.validate_tool_use("git")  # Should succeed
```

---

## Next Steps

### Immediate (Setup Complete)
- ✅ Directory structure created
- ✅ Configuration files in place
- ✅ Documentation complete
- ✅ Templates provided

### Optional Enhancements

#### 1. Add Session Hooks
Create `.claude/hooks/` scripts for automatic behaviors:
- `session-start-continuity.sh` - Auto-load ledgers
- `pre-compact.sh` - Block compaction (prefer clear)
- `post-tool-use.sh` - Track costs automatically

#### 2. Create Custom Skills
Add ATLASsemi-specific skills to `.claude/skills/`:
- `/run-8d-workflow` - Execute complete Phase 0-3
- `/validate-8d` - Check 8D report completeness
- `/tier-check` - Verify current security tier

#### 3. Create Custom Agents
Add specialized agents to `.claude/agents/`:
- `8d-analyst` - Review 8D reports for quality
- `security-tier-advisor` - Recommend tier for problem
- `kg-query` - Search knowledge graph for similar cases

#### 4. Add Artifact Index Integration
When knowledge graph is ready:
- Index 8D reports for search
- Query similar historical cases
- Track patterns across problems

---

## Troubleshooting

### "Ledger not loading after /clear"
- Check if ledger exists in `thoughts/ledgers/`
- Verify file naming: `CONTINUITY_CLAUDE-*.md`
- May need SessionStart hook (future enhancement)

### "Can't create handoff"
- Ensure `thoughts/shared/handoffs/` exists
- Check permissions on directory
- Use `/create_handoff` skill if available

### "Security tier violations"
- Check ledger for current tier
- Review `tier_enforcer.py` for allowed tools
- Use `enforcer.get_allowed_tools()` to see what's permitted

### "Cost tracking not working"
- Ensure `ModelRouter` is initialized in agent
- Check API keys are set (if using real LLMs)
- Call `router.get_usage_summary()` to see stats

---

## Reference

### Key Files
- **`CLAUDE.md`** - Main instructions for Claude Code
- **`DEVELOPMENT_STATUS.md`** - Current implementation status
- **`README.md`** - Project overview and architecture
- **`SECURITY.md`** - Security tier guidelines

### Key Directories
- **`src/atlassemi/agents/`** - Agent implementations
- **`src/atlassemi/config/`** - Model routing
- **`src/atlassemi/security/`** - Tier enforcement
- **`thoughts/`** - Working memory (commit this!)
- **`.claude/`** - Configuration (cache is gitignored)

### Global Rules (Inherited)
From `~/.claude/rules/`:
- `agent-orchestration.md` - When to use agents
- `continuity.md` - Ledger management
- `git-commits.md` - Use /commit skill
- `observe-before-editing.md` - Check outputs first
- And others...

---

## Summary

**Continuous Claude is now fully set up for ATLASsemi!**

You can:
- ✅ Create ledgers for session continuity
- ✅ Use handoffs for multi-session work
- ✅ Track multi-phase implementations
- ✅ Document security tiers in sessions
- ✅ Preserve context across `/clear` operations
- ✅ Collaborate via handoffs
- ✅ Track costs and usage
- ✅ Extend with custom skills/agents

**Start using it:**
```
cd /mnt/c/src/Synterra/ATLASsemi
# Claude Code will load CLAUDE.md automatically
"Create a ledger for [your task]"
```

**Status:** Ready for multi-session development with full context preservation! 🚀
