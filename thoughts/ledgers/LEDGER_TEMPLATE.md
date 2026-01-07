# Continuity Ledger Template

Copy this template when starting a new session with complex work.

**File naming:** `CONTINUITY_CLAUDE-<session-name>.md`

---

```yaml
---
session_name: descriptive-name
problem_mode: excursion|improvement|operations
security_tier: general_llm|confidential_fab|top_secret
api_routing: anthropic|factory_genai|onprem
started: YYYY-MM-DD
last_updated: YYYY-MM-DD HH:MM
---
```

## Goal

What does "done" look like for this session?

- Success criteria
- Deliverables
- Quality gates

## Constraints

Technical requirements and limitations:

- Security tier restrictions (what tools are allowed/blocked)
- Time constraints
- Resource limitations
- Dependencies

## State

Multi-phase tracking with checkboxes:

- Done:
  - [x] Phase 1: Setup and initialization
  - [x] Phase 2: Core implementation
- Now: [→] Phase 3: Testing and validation
- Next: Phase 4: Documentation
- Remaining:
  - [ ] Phase 5: Integration
  - [ ] Phase 6: Review

## Key Decisions

Document important choices with rationale:

1. **Decision:** Chose dev mode over runtime mode for testing
   - **Rationale:** 10x cheaper, adequate for development
   - **Impact:** Lower cost, faster iteration

2. **Decision:** Using Tier 1 (General LLM) for initial development
   - **Rationale:** No proprietary data yet
   - **Impact:** Full external API access

## Open Questions

Track uncertainties:

- UNCONFIRMED: Should we use Neo4j or alternative for knowledge graph?
- UNCONFIRMED: What's the expected problem volume per day?

## Working Set

Files and commands in active use:

**Files:**
- `src/atlassemi/agents/narrative_agent.py`
- `src/atlassemi/config/model_router.py`
- `cli.py`

**Branch:** `main`

**Commands:**
```bash
python cli.py
pytest tests/
black . && isort .
```

## Progress Notes

Brief notes on what happened each session:

### 2026-01-07
- Created model router with tier-aware routing
- Implemented Phases 0-2 agents
- Set up Continuous Claude infrastructure
- Next: Prevention agent and orchestrator

### 2026-01-08
- [Add notes here]

## Cost Tracking

Monitor LLM usage:

- Session cost so far: $X.XX
- Budget remaining: $X.XX
- Largest expense: [Operation name]

## Security Notes

For Tier 2/3 sessions:

- Audit trail enabled: Yes/No
- Data classification: [Type of data handled]
- Compliance requirements: [Any special requirements]
- Restricted operations: [What's been blocked]

---

**Remember:**
- Update ledger before `/clear`
- Mark phases complete as you finish them
- Document key decisions with rationale
- Track UNCONFIRMED items
